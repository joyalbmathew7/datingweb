from rest_framework.exceptions import ValidationError

from profiles.constants import MAX_PROFILE_PHOTOS
from profiles.models import ProfilePhoto
from profiles.services.image_compression import ImageCompressionService

class ProfilePhotoService:

    @staticmethod
    def upload_photo(
        profile,
        image,
        is_profile_picture=False,
        is_cover_photo=False,
    ):
        photo_count = ProfilePhoto.objects.filter(
            profile=profile,
        ).count()

        if photo_count >= MAX_PROFILE_PHOTOS:
            raise ValidationError(
                "You can have a maximum of 10 photos."
            )

        if is_profile_picture:
            ProfilePhoto.objects.filter(
                profile=profile,
                is_profile_picture=True,
            ).update(
                is_profile_picture=False
            )

        if is_cover_photo:
            ProfilePhoto.objects.filter(
                profile=profile,
                is_cover_photo=True,
            ).update(
                is_cover_photo=False
            )
        image = ImageCompressionService.compress_image(image)
        return ProfilePhoto.objects.create(
            profile=profile,
            image=image,
            is_profile_picture=is_profile_picture,
            is_cover_photo=is_cover_photo,
            is_approved=True,
        )

    @staticmethod
    def delete_photo(profile, photo):
        if photo.profile != profile:
            raise ValidationError(
                "You cannot delete this photo."
            )

        photo.delete()

    @staticmethod
    def set_profile_picture(profile, photo):

        if photo.profile != profile:
            raise ValidationError(
                "You cannot change this photo."
            )

        ProfilePhoto.objects.filter(
            profile=profile,
            is_profile_picture=True,
        ).update(
            is_profile_picture=False
        )

        photo.is_profile_picture = True
        photo.save(
            update_fields=["is_profile_picture"]
        )

        return photo