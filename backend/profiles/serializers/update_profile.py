from rest_framework import serializers

from profiles.models import Profile
from profiles.services.profile import ProfileService


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "display_name",
            "bio",
            "date_of_birth",
            "gender",
            "interested_in",
            "relationship_status",
            "country",
            "state",
            "city",
        )

    def update(self, instance, validated_data):
        return ProfileService.update_profile(
            instance=instance,
            validated_data=validated_data,
        )