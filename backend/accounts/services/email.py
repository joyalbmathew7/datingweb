from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .verification import VerificationService

User = get_user_model()


class EmailService:
    @staticmethod
    def send_password_reset_email(email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = (
            f"http://localhost:5173/reset-password/"
            f"?uid={uid}&token={token}"
        )

        send_mail(
            subject="Reset Your Password",
            message=f"Reset your password:\n\n{reset_link}",
            from_email="noreply@datingapp.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

    @staticmethod
    def send_verification_email(user):
        verification_link = (
            VerificationService.generate_verification_link(user)
        )

        send_mail(
            subject="Verify Your Email",
            message=(
                "Welcome!\n\n"
                "Click the link below to verify your email:\n\n"
                f"{verification_link}"
            ),
            from_email="noreply@datingapp.com",
            recipient_list=[user.email],
            fail_silently=False,
        )