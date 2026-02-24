from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    lesson_name = serializers.CharField(source="lesson.name", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_date",
            "payment",
            "payment_way",
            "course",
            "lesson",
            "course_name",
            "lesson_name",
        )


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
