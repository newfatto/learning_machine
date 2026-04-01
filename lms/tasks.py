from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from lms.models import Course
from users.models import Subscription

User = get_user_model()


@shared_task
def send_course_update_email_task(course_id: int) -> None:
    """
    Отправляет уведомления подписанным пользователям об обновлении курса.
    """
    course = Course.objects.get(pk=course_id)

    subscriptions = Subscription.objects.filter(course=course).select_related("user")

    emails: list[str] = [
        sub.user.email
        for sub in subscriptions
        if sub.user.email
    ]

    if not emails:
        return

    send_mail(
        subject=f"Обновление курса: {course.name}",
        message=f'Материалы курса "{course.name}" обновлены.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=True,
    )


@shared_task
def deactivate_inactive_users_task() -> int:
    """
    Деактивирует пользователей, которые не заходили более 30 дней.
    """
    threshold = timezone.now() - timedelta(days=30)

    users = User.objects.filter(
        is_active=True,
        last_login__isnull=False,
        last_login__lt=threshold,
    )

    updated_count = users.update(is_active=False)
    return updated_count