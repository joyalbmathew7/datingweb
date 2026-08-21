from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import MeView, RegisterView,LogoutView,ChangePasswordView,ForgotPasswordView,ResetPasswordView,VerifyEmailView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("logout/", LogoutView.as_view()),
    path(
    "change-password/",ChangePasswordView.as_view(),
    name="change-password",
),
path(
    "forgot-password/",
    ForgotPasswordView.as_view(),
    name="forgot-password",
),
path(
    "reset-password/",
    ResetPasswordView.as_view(),
    name="reset-password",
),
path(
    "verify-email/",
    VerifyEmailView.as_view(),
    name="verify-email",
),
]
