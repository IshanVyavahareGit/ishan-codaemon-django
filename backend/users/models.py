from django.db import models

class AppUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserAudio(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="audios")
    file = models.FileField(upload_to="user_audio/")
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]  # newest first

    def __str__(self):
        return f"{self.user.name} ({'active' if self.is_active else 'inactive'})"


