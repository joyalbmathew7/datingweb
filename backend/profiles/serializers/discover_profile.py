from rest_framework import serializers

from profiles.models import Profile


class DiscoverProfileSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Profile

        fields = (
            "uuid",
            "display_name",
            "bio",
            "gender",
            "relationship_status",
        )