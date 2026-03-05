from rest_framework import serializers
from typing import Any

from lms.models import Course, Lesson
from users.models import Payment, Subscription, User


class PaymentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    lesson_name = serializers.CharField(source="lesson.name", read_only=True)
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_date",
            "amount",
            "payment_way",
            "course",
            "lesson",
            "course_name",
            "lesson_name",
            "session_id",
            "link",
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        course = attrs.get("course")
        lesson = attrs.get("lesson")

        if course and lesson:
            raise serializers.ValidationError(
                "Нужно указать либо course, либо lesson, но не оба одновременно."
            )

        if not course and not lesson:
            raise serializers.ValidationError(
                "Нужно указать, за что платёж: course или lesson."
            )

        return attrs

    def create(self, validated_data: dict[str, Any]) -> Payment:
        """
        Создаёт Payment и автоматически проставляет amount из цены курса/урока.
        """
        course: Course | None = validated_data.get("course")
        lesson: Lesson | None = validated_data.get("lesson")

        item = course or lesson
        if item is None:
            raise serializers.ValidationError("Нужно указать course или lesson.")

        amount_rub = item.price

        validated_data["amount"] = amount_rub
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "city",
            "avatar",
            "payments",
            "courses",
            "lessons",
        )


class UserPublicSerializer(serializers.ModelSerializer):
    """Публичная информация профиля (для просмотра чужих профилей)."""

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "city",
            "avatar",
            "courses",
            "lessons",
        )
        read_only_fields = fields


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar")

    def create(self, validated_data: dict) -> User:
        """
        Создаёт пользователя через менеджер, чтобы пароль сохранился в хэшированном виде.
        """
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ("id", "course")
