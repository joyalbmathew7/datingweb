from rest_framework import serializers

from profiles.models import Profile
from profiles.services.profile import ProfileService


class CreateProfileSerializer(serializers.ModelSerializer):
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

        return ProfileService.create_profile(
            user=user,
            validated_data=validated_data,
        )