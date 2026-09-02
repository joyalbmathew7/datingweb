from rest_framework import serializers

from notifications.models import Notification
from notifications.services import notification_payload


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    conversation_uuid = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            "uuid", "notification_type", "is_read", "created_at", "actor", "conversation_uuid"
        )
        read_only_fields = fields

    def get_actor(self, obj):
        return notification_payload(obj)["actor"]

    def get_conversation_uuid(self, obj):
        return str(obj.conversation.uuid) if obj.conversation else None
