from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from profiles.models import ProfilePhoto
from profiles.serializers import ProfilePhotoSerializer
from profiles.services.profile import ProfileService


class UploadPhotoView(generics.CreateAPIView):
    queryset = ProfilePhoto.objects.all()
    serializer_class = ProfilePhotoSerializer
    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def perform_create(self, serializer):
        profile = ProfileService.get_my_profile(
            self.request.user
        )

        print("PROFILE:", profile)
        print("PROFILE ID:", profile.id)

        serializer.save(profile=profile)
    def post(self, request, *args, **kwargs):
        print("SERIALIZER:", self.get_serializer_class())
        print("SERIALIZER MODULE:", self.get_serializer_class().__module__)

        return super().post(request, *args, **kwargs)