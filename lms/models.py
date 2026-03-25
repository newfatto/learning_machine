from django.core.validators import MinValueValidator
from django.db import models

from config import settings


class Course(models.Model):
    """
    Модель курса.
    Поля: название, описание, превью.
    """

    name = models.CharField(
        unique=True,
        max_length=150,
        blank=False,
        null=False,
        verbose_name="Название",
        help_text="Название курса",
    )

    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Описание курса"
    )

    preview = models.ImageField(
        upload_to="lms/courses/preview/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите картинку",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Автор",
        related_name="courses",
    )

    price = models.PositiveIntegerField(
        default=0, verbose_name="Цена", help_text="Стоимость урока"
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Модель урока.
    Поля: название, описание, превью, ссылка на видео, курс (к которому относится урок).
    """

    name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name="Название",
        help_text="Название урока",
    )

    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Описание урока"
    )

    price = models.PositiveIntegerField(
        default=0, verbose_name="Цена", help_text="Стоимость урока"
    )

    preview = models.ImageField(
        upload_to="lms/lessons/preview/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите картинку",
    )

    video_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Вставьте ссылку на видео урока",
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Автор",
        related_name="lessons",
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        return self.name
