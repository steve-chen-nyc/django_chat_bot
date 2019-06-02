from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Client, Project
import json

class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat'
        self.name = ""

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': "Please provide your name to get started.",
            'bot': True
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        if self.name:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'bot_message',
                    'message': message
                }
            )
        else:
            self.name = json.loads(text_data)['message']

            message = "Thanks " + self.name + ". What can i do for you?"

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': json.loads(text_data)['message']
                }
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'bot_greeting',
                    'message': message
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'bot': False,
            'userName': self.name
        }))


    # Receive message from room group
    async def bot_greeting(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'bot': True
        }))


    # Receive message from room group
    async def bot_message(self, event):
        message = "Perfect! Let me looks this up.... \n"
        client = Client.objects.get(name=self.name)
        projects = client.project_set.all()

        if projects.count() > 0:
            message = message + "you have " + str(projects.count()) + " projects \n"

            for project in projects:
                message = message + project.name + "\n"

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'bot': True
            }))
