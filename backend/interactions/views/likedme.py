from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from interactions.services.liked_me import LikedMeService
from profiles.serializers.discover_profile import (
    DiscoverProfileSerializer,
)


class LikedMeView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DiscoverProfileSerializer

    def get_queryset(self):
        return LikedMeService.get_liked_me(
            self.request.user
        )