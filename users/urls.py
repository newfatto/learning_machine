from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentDestroyAPIView,
                         PaymentListAPIView, PaymentRetrieveAPIView,
                         PaymentSerializer, PaymentUpdateAPIView, UserViewSet)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment-get"),
    path(
        "payment/update/<int:pk>/",
        PaymentUpdateAPIView.as_view(),
        name="payment-update",
    ),
    path(
        "payment/delete/<int:pk>/",
        PaymentDestroyAPIView.as_view(),
        name="payment-delete",
    ),
] + router.urls
