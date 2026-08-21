from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model.

    We inherit from AbstractUser so we keep Django's
    authentication system while allowing future customization.
    """
    pass