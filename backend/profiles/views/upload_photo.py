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

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["profile"] = ProfileService.get_my_profile(
            self.request.user
        )

        return context