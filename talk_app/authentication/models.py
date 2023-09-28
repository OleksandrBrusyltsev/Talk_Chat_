from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
