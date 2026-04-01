from django.urls import path
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentCreateAPIView,
    PaymentDestroyAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    PaymentStatusAPIView,
    PaymentUpdateAPIView,
    SubscriptionAPIView,
    UserViewSet,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(
            permission_classes=[
                AllowAny,
            ]
        ),
        name="refresh_token",
    ),
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
    path(
        "payment/status/<int:pk>/",
        PaymentStatusAPIView.as_view(),
        name="payment-status",
    ),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
] + router.urls
