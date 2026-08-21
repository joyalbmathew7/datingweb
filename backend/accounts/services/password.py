from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class PasswordService:
    @staticmethod
    def change_password(user, new_password):
        user.set_password(new_password)
        user.save(update_fields=["password"])
        return user

    @staticmethod
    def reset_password(user_model, uid, token, new_password):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = user_model.objects.get(pk=user_id)
        except Exception:
            return False

        if not PasswordResetTokenGenerator().check_token(user, token):
            return False

        validate_password(new_password, user)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return True