from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.permissions import IsSelf
from users.serializers import (
    PaymentSerializer,
    UserCreateSerializer,
    UserPublicSerializer,
    UserSerializer,
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
    serializer_class = PaymentSerializer


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
