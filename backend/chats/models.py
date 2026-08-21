from django.db import models

from interactions.models import Match
from profiles.models import Profile
import uuid

class Conversation(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name="conversation",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.match.profile_one.display_name} "
            f"↔ "
            f"{self.match.profile_two.display_name}"
        )


class Message(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.sender.display_name}: "
            f"{self.content[:30]}"
        )