from rest_framework.exceptions import ValidationError

from interactions.models import Interaction, Match
from profiles.services.profile import ProfileService
from chats.models import Conversation
from notifications.models import Notification
from notifications.services import create_notification

class InteractionService:

    @staticmethod
    def create_interaction(
        user,
        target_profile,
        action,
    ):
        from_profile = ProfileService.get_my_profile(user)

        if from_profile == target_profile:
            raise ValidationError(
                "You cannot interact with your own profile."
            )

        if action not in (
            Interaction.LIKE,
            Interaction.PASS,
            Interaction.UNLIKE,
        ):
            raise ValidationError(
                "Invalid interaction."
            )

        # UNLIKE
        if action == Interaction.UNLIKE:

            Interaction.objects.filter(
                from_profile=from_profile,
                to_profile=target_profile,
                action=Interaction.LIKE,
            ).delete()

            profile_one, profile_two = sorted(
                [from_profile, target_profile],
                key=lambda profile: profile.id,
            )

            Match.objects.filter(
                profile_one=profile_one,
                profile_two=profile_two,
            ).delete()

            return None, None

        # LIKE / PASS
        interaction, created = Interaction.objects.update_or_create(
            from_profile=from_profile,
            to_profile=target_profile,
            defaults={
                "action": action,
            },
        )
        if action == Interaction.LIKE and created:
            create_notification(
                recipient=target_profile,
                actor=from_profile,
                notification_type=Notification.LIKE,
            )

        # Check for a mutual like
        if action == Interaction.LIKE:

            mutual_like = Interaction.objects.filter(
                from_profile=target_profile,
                to_profile=from_profile,
                action=Interaction.LIKE,
            ).exists()

            if mutual_like:

                profile_one, profile_two = sorted(
                    [from_profile, target_profile],
                    key=lambda profile: profile.id,
                )

                match, match_created = Match.objects.get_or_create(
                    profile_one=profile_one,
                    profile_two=profile_two,
                )
                Conversation.objects.get_or_create(
                    match=match,
                )

                return interaction, match

        return interaction, None