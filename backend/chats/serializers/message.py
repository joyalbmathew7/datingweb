from rest_framework import serializers

from chats.models import Message


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "uuid",
            "sender",
            "content",
            "created_at",
        )

        read_only_fields = (
            "uuid",
            "sender",
            "created_at",
        )

    def get_sender(self, obj):
        return {
            "uuid": str(obj.sender.uuid),
            "display_name": obj.sender.display_name,
        }