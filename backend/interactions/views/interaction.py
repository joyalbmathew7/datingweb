from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from interactions.serializers import InteractionSerializer
from interactions.services import InteractionService
from profiles.models import Profile


class InteractionView(generics.CreateAPIView):

    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        target_profile = Profile.objects.get(
            uuid=serializer.validated_data[
                "profile_uuid"
            ]
        )

        interaction, match = InteractionService.create_interaction(
            user=request.user,
            target_profile=target_profile,
            action=serializer.validated_data["action"],
        )

        # UNLIKE
        if serializer.validated_data["action"] == "UNLIKE":
            return Response(
                {
                    "detail": "Interaction removed successfully.",
                },
                status=status.HTTP_200_OK,
            )

        response_data = {
            "detail": "Interaction saved successfully.",
            "uuid": str(interaction.uuid),
            "action": interaction.action,
        }

        if match:
            response_data["match"] = {
                "uuid": str(match.uuid),
                "profile_one": match.profile_one.display_name,
                "profile_two": match.profile_two.display_name,
            }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
        )