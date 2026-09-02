from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles.models import Profile
from profiles.serializers.profile_detail import ProfileDetailSerializer


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"

    def get_queryset(self):
        return Profile.objects.prefetch_related(
            "photos"
        )