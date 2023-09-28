from django.db import models

from talk_core import settings


class Channel(models.Model):
    image = models.ImageField(upload_to='profile_photos/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
