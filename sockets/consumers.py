import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ProjectConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None

    async def connect(self):
        project_id = self.scope['url_route']['kwargs']['project_id']
        self.group_name = f'project_{project_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.receive('connected')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'message',
                'message': text_data
            }
        )

    async def message(self, event):
        """Handle message type events."""
        message = event['message']
        await self.send(text_data=message)

    async def task_update(self, event):
        """Handle update_task type events."""
        await self._dispatch_message(event)

    async def task_create(self, event):
        """Handle create_task type events."""
        await self._dispatch_message(event)

    async def task_delete(self, event):
        """Handle delete_task type events."""
        await self._dispatch_message(event)

    async def _dispatch_message(self, message):
        await self.send(text_data=json.dumps(message))
