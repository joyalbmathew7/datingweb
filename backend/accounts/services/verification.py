from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

User = get_user_model()


class VerificationService:

    @staticmethod
    def generate_verification_link(user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        return (
            "http://localhost:5173/verify-email/"
            f"?uid={uid}&token={token}"
        )

    @staticmethod
    def verify_email(uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            return False

        if not default_token_generator.check_token(user, token):
            return False

        user.is_active = True
        user.save(update_fields=["is_active"])

        return True