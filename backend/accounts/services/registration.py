from django.contrib.auth import get_user_model

from accounts.services.otp import OTPService
from  accounts.models import EmailOTP
User = get_user_model()


class RegistrationService:

    @staticmethod
    def register_user(validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        OTPService.send_email_otp(
            user,
            EmailOTP.Purpose.EMAIL_VERIFICATION,
        )

        return user