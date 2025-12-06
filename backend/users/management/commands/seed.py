from django.core.management.base import BaseCommand
from users.models import AppUser


class Command(BaseCommand):
    help = "Seed sample users"

    def handle(self, *args, **kwargs):
        AppUser.objects.all().delete()
        AppUser.objects.create(name="Ishan", email="ishan@example.com", bio="AI Engineer")
        AppUser.objects.create(name="Rohit", email="rohit@example.com", bio="Backend Developer")
        AppUser.objects.create(name="Sara", email="sara@example.com", bio="Designer")
        self.stdout.write(self.style.SUCCESS("Successfully seeded users"))
