from rest_framework import serializers

from profiles.models import ProfilePhoto
from profiles.services.profile_photo import ProfilePhotoService


class ProfilePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfilePhoto
        fields = (
            "uuid",
            "image",
            "is_profile_picture",
            "is_cover_photo",
            "is_approved",
            "created_at",
        )

        read_only_fields = (
            "uuid",
            "is_approved",
            "created_at",
        )

    def create(self, validated_data):
        profile = self.context["profile"]

        return ProfilePhotoService.upload_photo(
            profile=profile,
            image=validated_data["image"],
            is_profile_picture=validated_data.get(
                "is_profile_picture",
                False,
            ),
            is_cover_photo=validated_data.get(
                "is_cover_photo",
                False,
            ),
        )