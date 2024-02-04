from unittest.mock import MagicMock, patch, AsyncMock

from django.test import TestCase

from core.sockets import sockets_utils
4

class TestSocketUtils(TestCase):
    def setUp(self):
        self.mock_channel_layer = AsyncMock()

        self.task = MagicMock(id=1, title='Test Task', description='Test Description', type=MagicMock(type='Test Type'),
                              status=MagicMock(status='OPEN'), assignee=MagicMock(username='testuser'),
                              project=MagicMock(id=1))

        self.data_dict = {
            'id': 1,
            'title': 'Test Task',
            'description': 'Test Description',
            'type': 'Test Type',
            'status': 'OPEN',
            'assignee': 'testuser',
            'project_id': 1
        }

    @patch('core.sockets.sockets_utils.get_channel_layer')
    def test_send_task_create_event(self, mock_get_channel_layer):
        mock_get_channel_layer.return_value = self.mock_channel_layer

        sockets_utils.send_task_create_event(self.task.project_id, self.task)

        self.mock_channel_layer.group_send.assert_called_once_with(
            f'project_{self.task.project_id}',
            {
                'type': 'task_create',
                'task': self.data_dict
            }
        )

    @patch('core.sockets.sockets_utils.get_channel_layer')
    def test_send_task_update_event(self, mock_get_channel_layer):
        mock_get_channel_layer.return_value = self.mock_channel_layer

        sockets_utils.send_task_update_event(self.task.project_id, self.task)

        self.mock_channel_layer.group_send.assert_called_once_with(
            f'project_{self.task.project_id}',
            {
                'type': 'task_update',
                'task': self.data_dict
            }
        )

    @patch('core.sockets.sockets_utils.get_channel_layer')
    def test_send_task_delete_event(self, mock_get_channel_layer):
        mock_get_channel_layer.return_value = self.mock_channel_layer

        sockets_utils.send_task_delete_event(self.task.project_id, self.task.id)

        self.mock_channel_layer.group_send.assert_called_once_with(
            f'project_{self.task.project_id}',
            {
                'type': 'task_delete',
                'task': {
                    'id': self.task.id
                }
            }
        )
