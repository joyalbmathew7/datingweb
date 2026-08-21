import uuid

from django.conf import settings
from django.db import models

from profiles.models import Profile


class Interaction(models.Model):

    LIKE = "LIKE"
    PASS = "PASS"
    UNLIKE = "UNLIKE"

    ACTION_CHOICES = (
        (LIKE, "Like"),
        (PASS, "Pass"),
        (UNLIKE,"Unlike")
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    from_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="sent_interactions",
    )

    to_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="received_interactions",
    )

    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_profile", "to_profile"],
                name="unique_profile_interaction",
            ),
        ]

    def __str__(self):
        return (
            f"{self.from_profile.display_name} "
            f"{self.action} "
            f"{self.to_profile.display_name}"
        )


class Match(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    profile_one = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="matches_as_one",
    )

    profile_two = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="matches_as_two",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile_one", "profile_two"],
                name="unique_profile_match",
            ),
        ]

    def __str__(self):
        return (
            f"{self.profile_one.display_name} "
            f"↔ "
            f"{self.profile_two.display_name}"
        )


class Block(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    from_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="blocks_given",
    )

    to_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="blocks_received",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_profile", "to_profile"],
                name="unique_profile_block",
            ),
        ]

    def __str__(self):
        return (
            f"{self.from_profile.display_name} "
            f"blocked "
            f"{self.to_profile.display_name}"
        )