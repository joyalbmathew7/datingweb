from interactions.models import Interaction
from profiles.models import Profile
from profiles.services.profile import ProfileService


class LikedMeService:

    @staticmethod
    def get_liked_me(user):

        my_profile = ProfileService.get_my_profile(user)

        # People who liked me
        liked_profile_ids = Interaction.objects.filter(
            to_profile=my_profile,
            action=Interaction.LIKE,
        ).values_list(
            "from_profile_id",
            flat=True,
        )

        # People I already liked
        my_liked_profile_ids = Interaction.objects.filter(
            from_profile=my_profile,
            action=Interaction.LIKE,
        ).values_list(
            "to_profile_id",
            flat=True,
        )

        return Profile.objects.filter(
            id__in=liked_profile_ids,
        ).exclude(
            id__in=my_liked_profile_ids,
        )