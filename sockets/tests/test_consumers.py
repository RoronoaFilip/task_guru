from django.test import TestCase

from sockets.consumers import ProjectConsumer


class ConsumersTestCase(TestCase):
    def setUp(self):
        self.consumer_stub = ConsumerSelfStub()
        self.project_consumer = ProjectConsumer()

    async def test_connect(self):
        self.consumer_stub.scope = {'url_route': {'kwargs': {'project_id': 1}}}

        await ProjectConsumer.connect(self.consumer_stub)

        self.assertEqual(self.consumer_stub.accept_called, True)
        self.assertEqual(self.consumer_stub.group_name, 'project_1')
        self.assertEqual(self.consumer_stub.channel_layer.add_group_name, 'project_1')
        self.assertEqual(self.consumer_stub.channel_layer.add_chanel_name, self.consumer_stub.channel_name)
        self.assertEqual(self.consumer_stub.receive_result, 'connected')

    async def test_disconnect(self):
        self.consumer_stub.group_name = 'project_1'
        self.consumer_stub.channel_name = 'test_channel_name'

        await ProjectConsumer.disconnect(self.consumer_stub, 123)

        self.assertEqual(self.consumer_stub.channel_layer.discard_group_name, self.consumer_stub.group_name)
        self.assertEqual(self.consumer_stub.channel_layer.discard_channel_name, self.consumer_stub.channel_name)

    async def test_receive(self):
        self.consumer_stub.group_name = 'project_1'
        self.consumer_stub.channel_name = 'test_channel_name'

        await ProjectConsumer.receive(self.consumer_stub, 'test_message')

        self.assertEqual(self.consumer_stub.channel_layer.send_group_name, self.consumer_stub.group_name)
        self.assertEqual(self.consumer_stub.channel_layer.send_message, {'type': 'message', 'message': 'test_message'})

    async def test_message(self):
        await ProjectConsumer.message(self.consumer_stub, {'message': 'test_message'})

        self.assertEqual(self.consumer_stub.send_result, 'test_message')

    async def test_task_update(self):
        await ProjectConsumer.task_update(self.consumer_stub, {'message': 'task_update_message'})

        self.assertEqual(self.consumer_stub.send_result, '{"message": "task_update_message"}')

    async def test_task_create(self):
        await ProjectConsumer.task_create(self.consumer_stub, {'message': 'task_create_message'})

        self.assertEqual(self.consumer_stub.send_result, '{"message": "task_create_message"}')

    async def test_task_delete(self):
        await ProjectConsumer.task_delete(self.consumer_stub, {'message': 'task_delete_message'})

        self.assertEqual(self.consumer_stub.send_result, '{"message": "task_delete_message"}')


class ChannelLayerStub:

    def __init__(self):
        self.add_group_name = None
        self.add_chanel_name = None

        self.discard_group_name = None
        self.discard_channel_name = None

        self.send_group_name = None
        self.send_message = None

    async def group_add(self, group_name, channel_name):
        self.add_group_name = group_name
        self.add_chanel_name = channel_name

    async def group_discard(self, group_name, channel_name):
        self.discard_group_name = group_name
        self.discard_channel_name = channel_name

    async def group_send(self, group_name, message):
        self.send_group_name = group_name
        self.send_message = message


class ConsumerSelfStub(ProjectConsumer):
    def __init__(self):
        self.channel_name = 'test_channel_name'
        self.channel_layer = ChannelLayerStub()
        self.group_name = None
        self.receive_result = None
        self.accept_called = False
        self.send_result = None

    async def accept(self, subprotocol=None):
        self.accept_called = True

    async def receive(self, text_data):
        self.receive_result = text_data

    async def send(self, text_data=None, bytes_data=None, close=False):
        self.send_result = text_data
