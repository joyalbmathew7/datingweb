from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles.models import ProfilePhoto
from profiles.services.profile import ProfileService
from profiles.services.profile_photo import ProfilePhotoService
from rest_framework.response import Response

class SetProfilePictureView(generics.GenericAPIView):
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

    def patch(self, request, *args, **kwargs):
        photo = self.get_object()

        profile = ProfileService.get_my_profile(
            request.user
        )

        photo = ProfilePhotoService.set_profile_picture(
            profile=profile,
            photo=photo,
        )

        return Response({
            "detail": "Profile picture updated successfully.",
            "uuid": str(photo.uuid),
            "is_profile_picture": photo.is_profile_picture,
        })