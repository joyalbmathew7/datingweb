from rest_framework import serializers

from interactions.models import Match


class MatchSerializer(serializers.ModelSerializer):

    matched_profile = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = (
            "uuid",
            "matched_profile",
            "created_at",
        )

    def get_matched_profile(self, obj):
        my_profile = self.context["profile"]

        if obj.profile_one == my_profile:
            return {
                "uuid": str(obj.profile_two.uuid),
                "display_name": obj.profile_two.display_name,
            }

        return {
            "uuid": str(obj.profile_one.uuid),
            "display_name": obj.profile_one.display_name,
        }