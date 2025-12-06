from django.urls import path
from .views import (
    UserListAPIView,
    UserDetailAPIView,
    UserAudioAPIView,
    DashboardView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),  # frontend route
    path("users/", UserListAPIView.as_view()),
    path("users/<int:pk>/", UserDetailAPIView.as_view()),
    path("users/<int:pk>/audio/", UserAudioAPIView.as_view()),
]