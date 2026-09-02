from rest_framework import serializers
from django.db import transaction

from profiles.models import Profile
from profiles.services.profile import ProfileService
from profiles.services.profile_photo import ProfilePhotoService


class CreateProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Profile
        exclude = (
            "id",
            "uuid",
            "user",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        image = validated_data.pop("image")

        with transaction.atomic():
            profile = ProfileService.create_profile(
                user=user,
                validated_data=validated_data,
            )
            ProfilePhotoService.upload_photo(
                profile=profile,
                image=image,
                is_profile_picture=True,
            )

        return profile