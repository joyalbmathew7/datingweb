from rest_framework import serializers

from profiles.models import Profile
from profiles.serializers.profile_photo import ProfilePhotoSerializer


class DiscoveryProfileSerializer(serializers.ModelSerializer):
    photos = ProfilePhotoSerializer(many=True, read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)
    state_name = serializers.CharField(source="state.name", read_only=True)
    city_name = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "display_name",
            "bio",
            "date_of_birth",
            "gender",
            "interested_in",
            "relationship_status",
            "country",
            "state",
            "city",
            "country_name",
            "state_name",
            "city_name",
            "photos",
        )
        read_only_fields = fields