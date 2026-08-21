from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError

from profiles.models import Profile


class ProfileService:

    @staticmethod
    def create_profile(user, validated_data):
        if Profile.objects.filter(user=user).exists():
            raise ValidationError(
                "You already have a profile."
            )

        return Profile.objects.create(
            user=user,
            **validated_data,
        )

    @staticmethod
    def get_my_profile(user):
        return get_object_or_404(
            Profile,
            user=user,
        )
    @staticmethod
    def update_profile(instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance