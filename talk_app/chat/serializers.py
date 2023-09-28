from channels_main.models import Channel
from .models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password"]




class ChannelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Channel
        fields = ['id', 'title', 'image', 'owner', 'description', 'created_at']


class MessageSerializer(serializers.Serializer):
    text = serializers.CharField()
    channelId = serializers.IntegerField()
    createdAt = serializers.DateTimeField()
    owner = UserSerializer()
