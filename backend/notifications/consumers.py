import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from profiles.models import Profile


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await self.get_user_from_token()
        if user is None:
            await self.close()
            return

        profile = await self.get_profile(user)
        if profile is None:
            await self.close()
            return

        self.group_name = f"notifications_{profile.uuid}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notification_created(self, event):
        await self.send(text_data=json.dumps({"type": "notification", **event["notification"]}))

    async def get_user_from_token(self):
        try:
            query = self.scope["query_string"].decode()
            if not query.startswith("token="):
                return None
            user_id = AccessToken(query.split("=", 1)[1])["user_id"]
            return await self.get_user(user_id)
        except Exception:
            return None

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_profile(self, user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return None
