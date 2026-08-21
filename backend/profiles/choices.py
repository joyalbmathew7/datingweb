from django.db import models


class Gender(models.TextChoices):
    MAN = "MAN", "Man"
    WOMAN = "WOMAN", "Woman"
    NON_BINARY = "NON_BINARY", "Non-binary"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY", "Prefer not to say"


class InterestedIn(models.TextChoices):
    MEN = "MEN", "Men"
    WOMEN = "WOMEN", "Women"
    EVERYONE = "EVERYONE", "Everyone"


class RelationshipStatus(models.TextChoices):
    SINGLE = "SINGLE", "Single"
    IN_RELATIONSHIP = "IN_RELATIONSHIP", "In a Relationship"