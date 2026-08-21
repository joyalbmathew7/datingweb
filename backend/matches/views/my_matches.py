from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import models
from interactions.models import Match
from profiles.services.profile import ProfileService
from matches.serializers import MatchSerializer


class MyMatchesView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = ProfileService.get_my_profile(
            self.request.user
        )

        return Match.objects.filter(
            models.Q(profile_one=profile)
            | models.Q(profile_two=profile)
        ).order_by("-created_at")

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["profile"] = ProfileService.get_my_profile(
            self.request.user
        )

        return context