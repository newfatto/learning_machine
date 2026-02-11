from django.db import models

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


    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        return self.name

# Урок:    название,    описание,    превью(картинка),    ссылка    на    видео.
