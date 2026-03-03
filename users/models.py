from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    """Менеджер пользователя с авторизацией по email"""

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        """
        Создание обычного пользователя
        """
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        """
        Создание суперпользователя
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Поля: Почта, Телефон, Город, Аватар.
    Авторизация по email.
    """

    objects = UserManager()
    username = None
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=False,
        null=False,
        verbose_name="email",
        help_text="Адрес электронной почты",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Номер телефона",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите город",
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAY_CHOICES = [
        ("cash", "наличные"),
        ("transfer", "перевод на счёт"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь",
        related_name="payments",
    )
    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата платежа")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Курс",
        related_name="payments",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Урок",
        related_name="payments",
    )
    payment = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Сумма платежа",
        help_text="Введите сумму платежа",
    )
    payment_way = models.CharField(
        max_length=10,
        choices=PAY_CHOICES,
        default="cash",
        verbose_name="Способ платежа",
        help_text="Укажите способ совершения платежа",
    )

    class Meta:
        verbose_name = "платёж"
        verbose_name_plural = "платежи"

    def __str__(self):
        item = self.course or self.lesson
        return f"{self.user.email} — {item} — {self.payment}₽"


class Subscription(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscriptions",
    )

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_user_course_subscription"
            )
        ]

    def __str__(self):
        return f"{self.user} — {self.course}"
