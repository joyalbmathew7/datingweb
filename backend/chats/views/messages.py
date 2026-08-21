from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from interactions.models import Block
from chats.models import Conversation
from chats.serializers.message import MessageSerializer
from profiles.services.profile import ProfileService
from interactions.models import Block

class ConversationMessagesView(generics.ListCreateAPIView):

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_conversation(self):
        profile = ProfileService.get_my_profile(
            self.request.user
        )

        try:
            return Conversation.objects.get(
                uuid=self.kwargs["uuid"],
                match__profile_one=profile,
            )
        except Conversation.DoesNotExist:
            try:
                return Conversation.objects.get(
                    uuid=self.kwargs["uuid"],
                    match__profile_two=profile,
                )
            except Conversation.DoesNotExist:
                raise ValidationError(
                    "You cannot access this conversation."
                )

    def get_queryset(self):
        conversation = self.get_conversation()

        return conversation.messages.all().order_by(
            "created_at"
        )

    def perform_create(self, serializer):
        conversation = self.get_conversation()

        profile = ProfileService.get_my_profile(
            self.request.user
        )

        other_profile = (
            conversation.match.profile_two
            if conversation.match.profile_one == profile
            else conversation.match.profile_one
        )

        is_blocked = Block.objects.filter(
            from_profile=profile,
            to_profile=other_profile,
        ).exists() or Block.objects.filter(
            from_profile=other_profile,
            to_profile=profile,
        ).exists()

        if is_blocked:
            raise ValidationError(
                "You cannot send messages because this user is blocked."
            )

        serializer.save(
            conversation=conversation,
            sender=profile,
        )