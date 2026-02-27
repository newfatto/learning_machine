from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создаёт суперпользователя user2@user2.user2, если его нет."

    def handle(self, *args, **options) -> None:
        email = "user2@user2.user2"
        password = "user2"

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_password(password)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Суперпользователь готов: {email}"))
