from authentication.constans import cloudinary_base_url, kiev
from chat.models import Message
from channels_main.models import Channel
from authentication.models import CustomUser
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import QueryDict
import json
from datetime import datetime
from pytz import timezone

@database_sync_to_async
def create_message(text, user, channel):
    return Message.objects.create(
        text=text,
        owner=user,
        channel=channel
    )
####
@database_sync_to_async
def get_user(user_id):
    return CustomUser.objects.get(id=user_id)

@database_sync_to_async
def get_messages(channel):
    return list(Message.objects.filter(channel=channel).values(
        'id', 'text', 'owner__id', 'owner__profile_photo', 'owner__username', 'owner__email', 'created_at'
    ))



@database_sync_to_async
def get_channel(channel_id):
    return Channel.objects.get(id=channel_id)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get('query_string').decode('utf-8')
        query_params = QueryDict(query_string=query_string, mutable=False)
        token = query_params.get('token', None)
        channel_id = query_params.get('channel_id', None)

        if token:
            try:
                decoded_data = UntypedToken(token).payload
                user_id = decoded_data.get("user_id")

                if user_id:
                    self.scope['user'] = await get_user(user_id)
                else:
                    await self.close()
                    return
            except (InvalidToken, TokenError):
                await self.close()
                return

        if not self.scope['user'] or not channel_id:
            await self.close()
            return

        self.channel = await get_channel(channel_id)

        await self.channel_layer.group_add(
            str(self.channel.id),
            self.channel_name
        )

        await self.accept()

        messages = await get_messages(self.channel)

        for message in messages:
            full_profile_photo_url = cloudinary_base_url + message['owner__profile_photo'] if message[
                'owner__profile_photo'] else None
            await self.send(text_data=json.dumps({
                'message_id': message['id'],  # ID сообщения
                'user_id': message['owner__id'],  # ID пользователя
                'profile_photo': full_profile_photo_url,  # фото пользователя
                'message': message['text'],
                'username': message['owner__username'],
                'email': message['owner__email'],
                'created_at': message['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            str(self.channel.id),
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        user = self.scope['user']

        message = await create_message(message_text, user, self.channel)
        full_profile_photo_url = cloudinary_base_url + (user.profile_photo.url if user.profile_photo else "")

        await self.channel_layer.group_send(
            str(self.channel.id),
            {
                'type': 'chat_message',
                'message_id': message.id,
                'user_id': user.id,
                'profile_photo': user.profile_photo.url,  # фото пользователя
                'message': message.text,
                'username': user.username,
                'email': user.email,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )





    async def chat_message(self, event):

        utc_time_str = event['created_at']
        utc_time = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')
        utc_time = timezone('UTC').localize(utc_time)
        kiev_time = utc_time.astimezone(kiev)
        kiev_time_str = kiev_time.strftime('%Y-%m-%d %H:%M:%S')



        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'email': event['email'],
            'created_at': kiev_time_str,
            'type': 'sender',
            'user_id': event.get('user_id', None),
            'message_id': event.get('message_id', None),
            'profile_photo': event.get('profile_photo', None),
        }))