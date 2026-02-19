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
        fields = "__all__"
