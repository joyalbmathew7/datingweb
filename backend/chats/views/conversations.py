from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from chats.models import Conversation
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

        return Conversation.objects.filter(
            match__profile_one=profile
        ) | Conversation.objects.filter(
            match__profile_two=profile
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["profile"] = self.get_profile()

        return context