from rest_framework import serializers
from profiles.models import Profile


class DiscoveryProfileSerializer(serializers.ModelSerializer):

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
        )
        read_only_fields = fields