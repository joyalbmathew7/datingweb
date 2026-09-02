from rest_framework import serializers

from interactions.models import Match


class MatchSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = (
            "uuid",
            "profile",
            "created_at",
        )

        read_only_fields = (
            "uuid",
            "profile",
            "created_at",
        )

    def get_profile(self, obj):
        current_profile = self.context["profile"]

        if obj.profile_one == current_profile:
            other_profile = obj.profile_two
        else:
            other_profile = obj.profile_one

        photo = (
            other_profile.photos.filter(is_profile_picture=True).first()
            or other_profile.photos.first()
        )
        image = None
        if photo:
            request = self.context.get("request")
            image = (
                request.build_absolute_uri(photo.image.url)
                if request
                else photo.image.url
            )

        return {
            "uuid": str(other_profile.uuid),
            "display_name": other_profile.display_name,
            "bio": other_profile.bio,
            "gender": other_profile.gender,
            "relationship_status": other_profile.relationship_status,
            "photo": image,
        }