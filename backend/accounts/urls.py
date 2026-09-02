from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    MeView,
    RegisterView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    VerifyEmailView,
    DeleteAccountView,
    ForgotPasswordOTPView,
    VerifyPasswordOTPView,
    ResetPasswordOTPView,
)


urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="refresh",
    ),

    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),

    # Email verification
    path(
        "verify-email/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),

    # Forgot password → OTP
    path(
        "forgot-password/",
        ForgotPasswordOTPView.as_view(),
        name="forgot-password",
    ),

    # Verify password-reset OTP
    path(
        "forgot-password/verify/",
        VerifyPasswordOTPView.as_view(),
        name="verify-password-otp",
    ),

    # Set new password
    path(
        "forgot-password/reset/",
        ResetPasswordOTPView.as_view(),
        name="reset-password-otp",
    ),

    # Delete account
    path(
        "account/",
        DeleteAccountView.as_view(),
        name="delete-account",
    ),
]