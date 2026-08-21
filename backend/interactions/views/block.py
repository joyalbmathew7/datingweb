from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from interactions.models import Block
from interactions.serializers.block import BlockSerializer
from interactions.services.block import BlockService
from profiles.models import Profile


class BlockView(generics.CreateAPIView):

    serializer_class = BlockSerializer
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

        BlockService.block_profile(
            user=request.user,
            target_profile=target_profile,
        )

        return Response(
            {
                "detail": "Profile blocked successfully."
            },
            status=status.HTTP_201_CREATED,
        )


class UnblockView(generics.CreateAPIView):

    serializer_class = BlockSerializer
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

        BlockService.unblock_profile(
            user=request.user,
            target_profile=target_profile,
        )

        return Response(
            {
                "detail": "Profile unblocked successfully."
            },
            status=status.HTTP_200_OK,
        )