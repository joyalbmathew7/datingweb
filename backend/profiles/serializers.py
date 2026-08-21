from rest_framework import serializers

from .models import Profile
from .services import ProfileService


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = (
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