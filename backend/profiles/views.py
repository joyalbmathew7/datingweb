from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .serializers import ProfileSerializer


class CreateProfileView(generics.CreateAPIView):

    queryset = Profile.objects.all()

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated,
    ]

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer
from .services import ProfileService


class MyProfileView(generics.RetrieveAPIView):

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return ProfileService.get_my_profile(
            self.request.user
        )