from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles.models import ProfilePhoto
from profiles.services.profile import ProfileService


class DeletePhotoView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    lookup_field = "uuid"
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        profile = ProfileService.get_my_profile(
            self.request.user
        )

        return ProfilePhoto.objects.filter(
            profile=profile
        )