from django.db.models import Q

from interactions.models import Interaction
from profiles.models import Profile
from profiles.choices import Gender, InterestedIn


class DiscoveryService:

    @staticmethod
    def get_discover_profiles(user):

        my_profile = Profile.objects.get(user=user)

        # --------------------------------
        # 1. Determine preferred genders
        # --------------------------------

        if my_profile.interested_in == InterestedIn.MEN:
            gender_filter = Q(gender=Gender.MAN)

        elif my_profile.interested_in == InterestedIn.WOMEN:
            gender_filter = Q(gender=Gender.WOMAN)

        else:
            gender_filter = Q(
                gender__in=[
                    Gender.MAN,
                    Gender.WOMAN,
                    Gender.NON_BINARY,
                ]
            )

        # --------------------------------
        # 2. Profiles already interacted with
        # --------------------------------

        interacted_profile_ids = Interaction.objects.filter(
            from_profile=my_profile,
        ).values_list(
            "to_profile_id",
            flat=True,
        )

        # --------------------------------
        # 3. Base queryset
        # --------------------------------

        profiles = Profile.objects.filter(
            gender_filter,
        ).exclude(
            id=my_profile.id,
        ).exclude(
            id__in=interacted_profile_ids,
        )

        # --------------------------------
        # LEVEL 1
        # Same city
        # --------------------------------

        same_city = profiles.filter(
            city=my_profile.city,
        ).order_by("?")

        # --------------------------------
        # LEVEL 2
        # Same state, different cities
        # --------------------------------

        same_state = profiles.filter(
            state=my_profile.state,
        ).exclude(
            city=my_profile.city,
        ).order_by("?")

        # --------------------------------
        # LEVEL 3
        # Other states
        # --------------------------------

        other_states = profiles.exclude(
            state=my_profile.state,
        ).order_by("?")

        return (
            list(same_city)
            + list(same_state)
            + list(other_states)
        )