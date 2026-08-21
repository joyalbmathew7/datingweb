from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles.serializers import UpdateProfileSerializer
from profiles.services.profile import ProfileService


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return ProfileService.get_my_profile(
            self.request.user
        )