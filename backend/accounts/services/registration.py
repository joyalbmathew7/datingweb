from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationService:
    @staticmethod
    def register_user(validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )