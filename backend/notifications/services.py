from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from notifications.models import Notification


def notification_payload(notification):
    photo = (
        notification.actor.photos.filter(is_profile_picture=True).first()
        or notification.actor.photos.first()
    )
    return {
        "uuid": str(notification.uuid),
        "type": notification.notification_type,
        "is_read": notification.is_read,
        "created_at": notification.created_at.isoformat(),
        "actor": {
            "uuid": str(notification.actor.uuid),
            "display_name": notification.actor.display_name,
            "photo": photo.image.url if photo else None,
        },
        "conversation_uuid": (
            str(notification.conversation.uuid) if notification.conversation else None
        ),
    }


def create_notification(*, recipient, actor, notification_type, conversation=None):
    if recipient == actor:
        return None

    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        notification_type=notification_type,
        conversation=conversation,
    )

    # A temporary Redis outage must not make likes or messages fail.
    try:
        async_to_sync(get_channel_layer().group_send)(
            f"notifications_{recipient.uuid}",
            {"type": "notification_created", "notification": notification_payload(notification)},
        )
    except Exception:
        pass

    return notification
