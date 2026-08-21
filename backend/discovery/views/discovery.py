from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from discovery.serializers import DiscoveryProfileSerializer
from discovery.services.discovery import DiscoveryService


class DiscoveryView(generics.ListAPIView):
    serializer_class = DiscoveryProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        filters = {
            "gender": self.request.query_params.get("gender"),
            "interested_in": self.request.query_params.get(
                "interested_in"
            ),
            "relationship_status": self.request.query_params.get(
                "relationship_status"
            ),
            "country": self.request.query_params.get(
                "country"
            ),
            "state": self.request.query_params.get(
                "state"
            ),
            "city": self.request.query_params.get(
                "city"
            ),
        }

        return DiscoveryService.get_profiles_for_user(
            self.request.user,
            filters=filters,
        )