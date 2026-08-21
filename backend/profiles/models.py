from django.conf import settings
from django.db import models
from .choices import (
    Gender,
    InterestedIn,
    RelationshipStatus,
)
from locations.models import Country, State, City
from common.models import BaseModel

from .constants import (
    MAX_DISPLAY_NAME_LENGTH,
    MAX_BIO_LENGTH,
    PROFILE_PHOTO_UPLOAD_PATH,
)
import uuid
# class Gender(models.TextChoices):
    # MAN = "MAN", "Man"
    # WOMAN = "WOMAN", "Woman"
    # NON_BINARY = "NON_BINARY", "Non-binary"
    # PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY", "Prefer not to say"
gender = models.CharField(
    max_length=20,
    choices=Gender.choices,
        )


# class InterestedIn(models.TextChoices):
    # MEN = "MEN", "Men"
    # WOMEN = "WOMEN", "Women"
    # EVERYONE = "EVERYONE", "Everyone"
interested_in = models.CharField(
    max_length=20,
    choices=InterestedIn.choices,
)

# class RelationshipStatus(models.TextChoices):
    # SINGLE = "SINGLE", "Single"
    # IN_RELATIONSHIP = "IN_RELATIONSHIP", "In a Relationship"
relationship_status = models.CharField(
    max_length=30,
    choices=RelationshipStatus.choices,
        )


class Profile(BaseModel):
    # uuid = models.UUIDField(
    # default=uuid.uuid4,
    # editable=False,
    # unique=True,
    #     )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    display_name = models.CharField(max_length=MAX_DISPLAY_NAME_LENGTH,)

    bio = models.TextField(max_length=MAX_BIO_LENGTH,blank=True)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
    )

    interested_in = models.CharField(
        max_length=20,
        choices=InterestedIn.choices,
    )

    relationship_status = models.CharField(
        max_length=30,
        choices=RelationshipStatus.choices,
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
    )

    state = models.ForeignKey(
        State,
        on_delete=models.PROTECT,
    )

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
    )

    # profile_photo = models.ImageField(
    #     upload_to=PROFILE_PHOTO_UPLOAD_PATH,
    #     blank=True,
    #     null=True,
    # )

    # cover_photo = models.ImageField(
    #     upload_to="cover_photos/",
    #     blank=True,
    #     null=True,
    # )

    # created_at = models.DateTimeField(
    #     auto_now_add=True,
    # )

    # updated_at = models.DateTimeField(
    #     auto_now=True,
    # )

    def __str__(self):
        return self.display_name



class ProfilePhoto(BaseModel):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    image = models.ImageField(
        upload_to=PROFILE_PHOTO_UPLOAD_PATH,
    )

    is_profile_picture = models.BooleanField(
        default=False,
    )

    is_cover_photo = models.BooleanField(
        default=False,
    )

    is_approved = models.BooleanField(
        default=False,
    )

    # uploaded_at = models.DateTimeField(
    #     auto_now_add=True,
    # )

    def __str__(self):
        return f"{self.profile.display_name}"