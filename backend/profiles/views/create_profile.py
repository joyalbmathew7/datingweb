from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles.models import Profile
from profiles.serializers import CreateProfileSerializer


class CreateProfileView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = [IsAuthenticated]