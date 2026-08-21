from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles.serializers import (
    DiscoverProfileSerializer,
)
from profiles.services.discovery import (
    DiscoveryService,
)


class DiscoverProfilesView(
    generics.ListAPIView
):
    serializer_class = (
        DiscoverProfileSerializer
    )

    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return DiscoveryService.get_discover_profiles(
            self.request.user
        )