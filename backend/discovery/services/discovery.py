from django.db.models import Case, IntegerField, Q, Value, When

from interactions.models import Interaction, Match
from profiles.models import Profile


class DiscoveryService:

    @staticmethod
    def get_profiles_for_user(
        user,
        filters=None,
    ):
        profile = Profile.objects.get(
            user=user
        )

        queryset = Profile.objects.exclude(
            user=user
        )

        # -------------------------
        # CUSTOM FILTERS
        # -------------------------

        if filters:

            if filters.get("search"):
                search = filters["search"].strip()
                queryset = queryset.filter(
                    Q(display_name__icontains=search)
                    | Q(bio__icontains=search)
                    | Q(city__name__icontains=search)
                    | Q(state__name__icontains=search)
                    | Q(country__name__icontains=search)
                )

            if filters.get("gender"):
                queryset = queryset.filter(
                    gender=filters["gender"]
                )

            if filters.get("interested_in"):
                queryset = queryset.filter(
                    interested_in=filters["interested_in"]
                )

            if filters.get("relationship_status"):
                queryset = queryset.filter(
                    relationship_status=filters[
                        "relationship_status"
                    ]
                )

            if filters.get("country"):
                queryset = queryset.filter(
                    country_id=filters["country"]
                )

            if filters.get("state"):
                queryset = queryset.filter(
                    state_id=filters["state"]
                )

            if filters.get("city"):
                queryset = queryset.filter(
                    city_id=filters["city"]
                )

        # -------------------------
        # REMOVE ALREADY INTERACTED
        # -------------------------
        if not (filters and filters.get("search")):
            interacted_profile_ids = Interaction.objects.filter(
                from_profile=profile,
            ).values_list(
                "to_profile_id",
                flat=True,
            )

            queryset = queryset.exclude(
                id__in=interacted_profile_ids
            )



        # -------------------------
        # REMOVE ALREADY MATCHED
        # -------------------------

        matched_profile_ids = Match.objects.filter(
            profile_one=profile,
        ).values_list(
            "profile_two_id",
            flat=True,
        )

        matched_profile_ids = matched_profile_ids.union(
            Match.objects.filter(
                profile_two=profile,
            ).values_list(
                "profile_one_id",
                flat=True,
            )
        )

        queryset = queryset.exclude(
            id__in=matched_profile_ids
        )

        # -------------------------A
        # LOCATION PRIORITY
        # -------------------------

        queryset = queryset.annotate(
            location_priority=Case(
                When(
                    city_id=profile.city_id,
                    then=Value(1),
                ),
                When(
                    state_id=profile.state_id,
                    then=Value(2),
                ),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by(
            "location_priority",
            "?",
        )

        return queryset


