from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch, Max

from chats.models import Conversation, Message
from chats.serializers.conversation import ConversationSerializer
from profiles.services.profile import ProfileService


class MyConversationsView(generics.ListAPIView):

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_profile(self):
        return ProfileService.get_my_profile(
            self.request.user
        )

    def get_queryset(self):
        profile = self.get_profile()

        # Get conversations for the user
        conversations = Conversation.objects.filter(
            match__profile_one=profile
        ) | Conversation.objects.filter(
            match__profile_two=profile
        )

        # Prefetch messages and sort by latest message
        messages_prefetch = Prefetch(
            'messages',
            queryset=Message.objects.order_by('-created_at')
        )

        # Annotate with latest message timestamp for sorting
        conversations = conversations.prefetch_related(
            messages_prefetch
        ).annotate(
            latest_message_at=Max('messages__created_at')
        ).order_by(
            '-latest_message_at',  # Most recent message first
            '-created_at'  # Fallback to conversation creation time
        )

        return conversations

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["profile"] = self.get_profile()

        return context