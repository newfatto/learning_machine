from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from lms.models import Course
from users.models import Payment, Subscription, User
from users.permissions import IsSelf
from users.serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
    SubscriptionSerializer,
    UserCreateSerializer,
    UserPublicSerializer,
    UserSerializer,
)
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
    retrieve_stripe_session,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer

        elif self.action == "retrieve":
            if self.get_object() == self.request.user:
                return UserSerializer
            return UserPublicSerializer

        elif self.action in ["update", "partial_update"]:
            return UserSerializer

        return UserPublicSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]

        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated]

        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsSelf]

        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer) -> None:
        payment = serializer.save(user=self.request.user, payment_way="transfer")
        course = payment.course

        product = create_stripe_product(name=course.name)
        price = create_stripe_price(amount=course.price, product_id=product["id"])

        session = create_stripe_session(
            price_id=price["id"],
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
        )

        payment.session_id = session["id"]
        payment.link = session["url"]
        payment.save()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("lesson", "course", "payment_way")
    ordering_fields = ("payment_date",)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()


class PaymentStatusAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk: int, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=pk)

        session = retrieve_stripe_session(payment.session_id)
        payment.status = session.get("payment_status")
        payment.save(update_fields=["status"])

        return Response(
            {
                "payment_id": payment.id,
                "session_id": payment.session_id,
                "status": payment.status,
            },
            status=status.HTTP_200_OK,
        )


class SubscriptionAPIView(APIView):
    """
    Управление подписками текущего пользователя.
    GET  - список подписок текущего пользователя
    POST - toggle подписки: если подписка есть -> удалить, иначе -> создать
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        subscriptions = Subscription.objects.filter(user=request.user).select_related(
            "course"
        )
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        course = request.data.get("course")

        if not course:
            return Response({"detail": "Поле course обязательно."}, status=400)

        course_item = get_object_or_404(Course, id=course)

        subs_qs = Subscription.objects.filter(user=user, course=course_item)

        if subs_qs.exists():
            subs_qs.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
