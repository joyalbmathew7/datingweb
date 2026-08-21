from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles.serializers import ProfileDetailSerializer
from profiles.services.profile import ProfileService


class MyProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return ProfileService.get_my_profile(
            self.request.user
        )