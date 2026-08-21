from rest_framework.exceptions import ValidationError

from interactions.models import Block
from profiles.services.profile import ProfileService


class BlockService:

    @staticmethod
    def block_profile(user, target_profile):

        from_profile = ProfileService.get_my_profile(
            user
        )

        if from_profile == target_profile:
            raise ValidationError(
                "You cannot block yourself."
            )

        block, created = Block.objects.get_or_create(
            from_profile=from_profile,
            to_profile=target_profile,
        )

        return block

    @staticmethod
    def unblock_profile(user, target_profile):

        from_profile = ProfileService.get_my_profile(
            user
        )

        Block.objects.filter(
            from_profile=from_profile,
            to_profile=target_profile,
        ).delete()