from rest_framework import serializers

from interactions.models import Interaction
from profiles.models import Profile


class InteractionSerializer(serializers.Serializer):

    profile_uuid = serializers.UUIDField()

    action = serializers.ChoiceField(
        choices=[
            Interaction.LIKE,
            Interaction.PASS,
            Interaction.UNLIKE,

        ]
    )

    def validate_profile_uuid(self, value):
        try:
            Profile.objects.get(uuid=value)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                "Profile does not exist."
            )

        return value