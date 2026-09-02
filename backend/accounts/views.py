from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiles.models import Profile

from .serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    ResetPasswordOTPSerializer,
    UserRegisterSerializer,
    UserSerializer,
    VerifyEmailSerializer,
    VerifyPasswordOTPSerializer,
)
from .services import EmailService, PasswordService, VerificationService
from .services.otp import OTPService
from accounts.models import EmailOTP

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK,

        )
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old_password": ["Old password is incorrect."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        PasswordService.change_password(
            user,
            serializer.validated_data["new_password"],
        )

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )


# class ForgotPasswordView(generics.GenericAPIView):
#     serializer_class = ForgotPasswordSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data["email"]

#         # Logic will come here

#         return Response(
#             {
#                 "message": "If an account exists with this email, a password reset email has been sent."
#             }
#         )


from .services import EmailService
class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        EmailService.send_password_reset_email(
            serializer.validated_data["email"]
            )
        return Response(
            {
                "message": (
                    "If an account exists with this email, "
                    "a password reset email has been sent."
                )
            }
        )



# class ResetPasswordView(generics.GenericAPIView):
#     serializer_class = ResetPasswordSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         success = PasswordService.reset_password(
#             user_model=User,
#             uid=serializer.validated_data["uid"],
#             token=serializer.validated_data["token"],
#             new_password=serializer.validated_data["new_password"],
#         )

#         if not success:
#             return Response(
#                 {"detail": "Invalid or expired reset link."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response(
#             {"message": "Password reset successfully."},
#             status=status.HTTP_200_OK,
#         )


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email or OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        OTPService.verify_email_otp(
            user=user,
            otp=otp,
            purpose=EmailOTP.Purpose.EMAIL_VERIFICATION,
        )

        user.email_verified = True
        user.save(update_fields=["email_verified"])

        return Response(
            {"message": "Email verified successfully."},
            status=status.HTTP_200_OK,
        )
                


class DeleteAccountView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # Delete uploaded profile photos from storage
        try:
            profile = user.profile

            for photo in profile.photos.all():
                if photo.image:
                    photo.image.delete(save=False)

        except Profile.DoesNotExist:
            pass

        # Delete the user and all CASCADE-related database records
        user.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class ForgotPasswordOTPView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if user:
            OTPService.send_email_otp(
                user,
                EmailOTP.Purpose.PASSWORD_RESET,
            )

        return Response(
            {
                "message": (
                    "If an account exists with this email, "
                    "a password reset OTP has been sent."
                )
            },
            status=status.HTTP_200_OK,
        )


class VerifyPasswordOTPView(generics.GenericAPIView):
    serializer_class = VerifyPasswordOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if not user:
            return Response(
                {"detail": "Invalid email or OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        OTPService.verify_email_otp(
            user=user,
            otp=otp,
            purpose=EmailOTP.Purpose.PASSWORD_RESET,
        )
        reset_token = OTPService.create_password_reset_token(user)


        return Response(
            {
                "message": "OTP verified successfully.",
                "reset_token": reset_token,

            },
            status=status.HTTP_200_OK,
        )

class ResetPasswordOTPView(generics.GenericAPIView):
    serializer_class = ResetPasswordOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if not user:
            return Response(
                {"detail": "Invalid password reset request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_record = OTPService.verify_password_reset_token(
            user=user,
            token=reset_token,
        )

        user.set_password(new_password)
        user.save(update_fields=["password"])

        # Make the reset token unusable
        token_record.delete()

        return Response(
            {
                "message": "Password reset successfully."
            },
            status=status.HTTP_200_OK,
        )