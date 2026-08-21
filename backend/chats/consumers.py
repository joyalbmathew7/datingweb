import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from chats.models import Conversation, Message
from interactions.models import Block
from profiles.models import Profile


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.conversation_uuid = (
            self.scope["url_route"]["kwargs"]["uuid"]
        )

        self.room_group_name = (
            f"chat_{self.conversation_uuid}"
        )

        # Authenticate JWT
        user = await self.get_user_from_token()

        if user is None:
            await self.close()
            return

        # Get user's profile
        self.profile = await self.get_profile(user)

        if self.profile is None:
            await self.close()
            return

        # Get conversation
        conversation = await self.get_conversation()

        if conversation is None:
            await self.close()
            return

        # Make sure this user belongs to the match
        if not await self.can_access_conversation(
            conversation
        ):
            await self.close()
            return

        # Join chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        content = data.get("content", "").strip()

        if not content:
            return

        conversation = await self.get_conversation()

        if conversation is None:
            return

        # Check block
        if await self.is_blocked(conversation):

            await self.send(
                text_data=json.dumps({
                    "type": "error",
                    "detail": (
                        "You cannot send messages "
                        "because this user is blocked."
                    ),
                })
            )

            return

        # Save message
        message = await self.create_message(
            conversation,
            self.profile,
            content,
        )

        # Send message to everyone in this conversation
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "uuid": str(message.uuid),
                "sender": {
                    "uuid": str(self.profile.uuid),
                    "display_name": (
                        self.profile.display_name
                    ),
                },
                "content": message.content,
                "created_at": (
                    message.created_at.isoformat()
                ),
            },
        )

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "message",
                "uuid": event["uuid"],
                "sender": event["sender"],
                "content": event["content"],
                "created_at": event["created_at"],
            })
        )

    # -------------------------
    # JWT
    # -------------------------

    async def get_user_from_token(self):

        try:
            query_string = (
                self.scope["query_string"]
                .decode()
            )

            if not query_string.startswith("token="):
                return None

            token = query_string.split(
                "=", 1
            )[1]

            access_token = AccessToken(token)

            user_id = access_token["user_id"]

            return await self.get_user(user_id)

        except Exception:
            return None

    @database_sync_to_async
    def get_user(self, user_id):

        try:
            return User.objects.get(
                id=user_id
            )
        except User.DoesNotExist:
            return None

    # -------------------------
    # Profile
    # -------------------------

    @database_sync_to_async
    def get_profile(self, user):

        try:
            return Profile.objects.get(
                user=user
            )
        except Profile.DoesNotExist:
            return None

    # -------------------------
    # Conversation
    # -------------------------

    @database_sync_to_async
    def get_conversation(self):

        try:
            return Conversation.objects.get(
                uuid=self.conversation_uuid
            )
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def can_access_conversation(
        self,
        conversation,
    ):

        return (
            conversation.match.profile_one_id
            == self.profile.id
            or
            conversation.match.profile_two_id
            == self.profile.id
        )

    # -------------------------
    # Block
    # -------------------------

    @database_sync_to_async
    def is_blocked(self, conversation):

        if (
            conversation.match.profile_one
            == self.profile
        ):
            other_profile = (
                conversation.match.profile_two
            )
        else:
            other_profile = (
                conversation.match.profile_one
            )

        return (
            Block.objects.filter(
                from_profile=self.profile,
                to_profile=other_profile,
            ).exists()
            or
            Block.objects.filter(
                from_profile=other_profile,
                to_profile=self.profile,
            ).exists()
        )

    # -------------------------
    # Save Message
    # -------------------------

    @database_sync_to_async
    def create_message(
        self,
        conversation,
        profile,
        content,
    ):

        return Message.objects.create(
            conversation=conversation,
            sender=profile,
            content=content,
        )