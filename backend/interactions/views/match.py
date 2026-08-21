from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from interactions.models import Match
from interactions.serializers import MatchSerializer
from profiles.services.profile import ProfileService


class MyMatchesView(generics.ListAPIView):

    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = ProfileService.get_my_profile(
            self.request.user
        )

        return Match.objects.filter(
            profile_one=profile
        ) | Match.objects.filter(
            profile_two=profile
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["profile"] = ProfileService.get_my_profile(
            self.request.user
        )

        return context