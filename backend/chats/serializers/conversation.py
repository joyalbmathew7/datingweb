from rest_framework import serializers

from chats.models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    last_message_at = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "uuid",
            "profile",
            "last_message",
            "last_message_at",
            "created_at",
        )

        read_only_fields = (
            "uuid",
            "profile",
            "last_message",
            "last_message_at",
            "created_at",
        )

    def get_profile(self, obj):
        current_profile = self.context["profile"]

        if obj.match.profile_one == current_profile:
            other_profile = obj.match.profile_two
        else:
            other_profile = obj.match.profile_one

        photo = (
            other_profile.photos.filter(is_profile_picture=True).first()
            or other_profile.photos.first()
        )
        image = None
        if photo:
            request = self.context.get("request")
            image = (
                request.build_absolute_uri(photo.image.url)
                if request
                else photo.image.url
            )

        return {
            "uuid": str(other_profile.uuid),
            "display_name": other_profile.display_name,
            "bio": other_profile.bio,
            "gender": other_profile.gender,
            "photo": image,
        }

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        if not last_msg:
            return None
        return {
            "content": last_msg.content,
            "sender_uuid": str(last_msg.sender.uuid),
            "created_at": last_msg.created_at.isoformat(),
        }

    def get_last_message_at(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        if not last_msg:
            return obj.created_at.isoformat()
        return last_msg.created_at.isoformat()