from django.db import models

from common.models import BaseModel
from profiles.models import Profile


class Notification(BaseModel):
    LIKE = "LIKE"
    MATCH = "MATCH"
    MESSAGE = "MESSAGE"
    TYPE_CHOICES = (
        (LIKE, "Like"),
        (MATCH, "Match"),
        (MESSAGE, "Message"),
    )

    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="notifications_sent"
    )
    notification_type = models.CharField(max_length=12, choices=TYPE_CHOICES)
    conversation = models.ForeignKey(
        "chats.Conversation",
        on_delete=models.CASCADE,
        related_name="notifications",
        blank=True,
        null=True,
    )
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
