from django.db import models

from authentication.models import CustomUser
from channels_main.models import Channel
from talk_core import settings


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Message from {self.owner.username} in channel {self.channel_id}"


class ImageModel(models.Model):
    file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.id} - {self.uploaded_at}"
