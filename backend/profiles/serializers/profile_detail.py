from rest_framework import serializers

from profiles.models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = (
            "id",
            "user",
        )