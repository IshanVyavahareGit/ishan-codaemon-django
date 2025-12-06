from rest_framework import serializers
from .models import AppUser, UserAudio


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["id", "name", "email", "bio"]


class UserAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAudio
        fields = ["id", "file", "is_active", "uploaded_at"]

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Max file size is 10MB.")
        if not value.content_type.startswith("audio/"):
            raise serializers.ValidationError("Only audio files are allowed.")
        return value
