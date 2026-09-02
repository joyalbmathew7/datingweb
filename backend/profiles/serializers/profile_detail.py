from rest_framework import serializers
from profiles.models import Profile, ProfilePhoto


class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = (
            "uuid",
            "image",
            "is_profile_picture",
            "is_cover_photo",
        )

class ProfileDetailSerializer(serializers.ModelSerializer):
    photos = ProfilePhotoSerializer(many=True, read_only=True)

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
            "photos",
        )