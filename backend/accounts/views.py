from django.contrib.auth import get_user_model
from rest_framework import generics, permissions,status
from .serializers import LogoutSerializer
from .serializers import UserRegisterSerializer, UserSerializer,ForgotPasswordSerializer,VerifyEmailSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import PasswordService

from .serializers import ResetPasswordSerializer
from .services import PasswordService

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


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
#----------------------------------------------------------------
from .serializers import ChangePasswordSerializer

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
                status=status.HTTP_400_BAD_REQUEST, #hashes the new password.
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



class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = PasswordService.reset_password(
            user_model=User,
            uid=serializer.validated_data["uid"],
            token=serializer.validated_data["token"],
            new_password=serializer.validated_data["new_password"],
        )

        if not success:
            return Response(
                {"detail": "Invalid or expired reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Password reset successfully."},
            status=status.HTTP_200_OK,
        )


from .services import VerificationService
class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = VerificationService.verify_email(
            uid=serializer.validated_data["uid"],
            token=serializer.validated_data["token"],
        )

        if not success:
            return Response(
                {"detail": "Invalid or expired verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Email verified successfully."}
        )