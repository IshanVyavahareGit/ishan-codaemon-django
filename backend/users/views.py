import os

from django.conf import settings  # optional, not strictly needed here
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AppUser, UserAudio
from .serializers import UserSerializer, UserAudioSerializer
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "users/dashboard.html"

class UserListAPIView(generics.ListCreateAPIView):
    """
    List all users or create a new user.
    /api/users/
    GET     - list users
    POST    - create a new user
    """
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a single user.
    GET, PUT, PATCH, DELETE /api/users/<pk>/
    """
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance: AppUser) -> None:
        """
        On user deletion, also remove all associated audio files from disk.

        The related UserAudio rows will be removed via the FK cascade, but Django
        does not automatically delete the underlying files, so we clean them up
        explicitly. This is defensive and works even if the user has no audio.
        """
        # Get related audios in a safe way
        audios_qs = getattr(instance, "audios", None)

        if audios_qs is not None:
            for audio in audios_qs.all():
                file_field = getattr(audio, "file", None)

                # Skip if there's no file associated
                if not file_field:
                    continue

                # Some broken rows may have a FileField with no actual file
                try:
                    file_path = file_field.path
                except (ValueError, AttributeError):
                    # in case 'file' attribute has no file associated with it.
                    continue

                # Remove file from disk if it exists
                if file_path and os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except FileNotFoundError:
                        # If file was already deleted manually, ignore
                        pass

        # Finally delete the user (and cascade its audio rows)
        instance.delete()



class UserAudioAPIView(APIView):
    """
    Manages the current active audio for a given user.

    A user can upload multiple audio files over time; only one is marked as
    active at any point. Older uploads are retained for history / audit but not returned by this endpoint.

    /api/users/<pk>/audio/
    GET     - returns the current active audio
    POST    - uploads a new audio, deactivates the older one
    DELETE  - deletes the current active audio

    /api/users/<pk>/audio/?history=1
    GET     - returns all audio uploads for the user, both active and inactive
    """

    def get(self, request, pk):
        """
        Returns the current active audio file for the given user.
        If no active audio exists, responds with 404.
        """
        user = get_object_or_404(AppUser, pk=pk)

        # If ?history=1 - return all audio uploads
        if request.query_params.get("history") == "1":
            queryset = user.audios.all()
            serializer = UserAudioSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Otherwise return only the active audio
        active_audio = user.audios.filter(is_active=True).first()
        if not active_audio:
            return Response(
                {"detail": "No audio uploaded"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserAudioSerializer(active_audio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """
        Uploads a new audio file for the given user.
        Any existing active audio records are marked inactive.
        The new upload becomes the single active audio for this user.
        """
        user = get_object_or_404(AppUser, pk=pk)

        # Deactivate any existing active audio for this user
        user.audios.filter(is_active=True).update(is_active=False)

        # Create a new active audio record
        serializer = UserAudioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        audio = serializer.save(user=user, is_active=True)

        response_serializer = UserAudioSerializer(audio)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """
        Deletes the current active audio for the given user.

        After deletion, if there are any historical audio records left,
        the most recently uploaded one is automatically promoted to active.

        The underlying file on disk for the deleted active audio is also removed.
        """
        user = get_object_or_404(AppUser, pk=pk)

        active_audio = user.audios.filter(is_active=True).first()
        if not active_audio:
            return Response(
                {"detail": "No active audio to delete"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Remove file from disk if it still exists
        if active_audio.file and os.path.isfile(active_audio.file.path):
            os.remove(active_audio.file.path)

        deleted_id = active_audio.id
        active_audio.delete()

        # Auto-promote latest remaining audio, if any
        # thanks to Meta.ordering = ["-uploaded_at"], first() == most recent
        next_audio = user.audios.first()
        promoted_id = None

        if next_audio:
            next_audio.is_active = True
            next_audio.save()
            promoted_id = next_audio.id

        detail_msg = (
            f"Active audio (id: {deleted_id}) deleted successfully."
        )

        if promoted_id is not None:
            detail_msg += f" Audio (id: {promoted_id}) promoted to active."

        return Response(
            {"detail": detail_msg},
            status=status.HTTP_200_OK,
        )