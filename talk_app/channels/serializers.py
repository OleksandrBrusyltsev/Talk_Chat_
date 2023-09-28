from rest_framework import serializers

from channels.models import Channel
from profiles.serializers import UserSerializer


class ChannelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Channel
        fields = ['id', 'title', 'image', 'owner', 'description',"created_at" ]
