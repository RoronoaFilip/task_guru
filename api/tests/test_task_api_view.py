from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

import api.tests.utils as test_utils
from core.models.project import Project
from core.models.task import Task, Type, Status


class TaskApiTest(TestCase):
    def setUp(self):
        # Create a tests user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.type = Type.objects.create(type='Test Type')
        self.status = Status.objects.create(status='OPEN')
        self.project = Project.objects.create(name='Test Project', description='Test Description', creator=self.user)

        self.task_data = {
            'id': 1,  # This is not used, but it's here to make the tests data complete
            'title': 'Test Task',
            'description': 'Test Description',
            'type': self.type,
            'status': self.status,
            'assignee': self.user,
            'creator': self.user,
            'project': self.project,
        }
        self.task = Task.objects.create(**self.task_data)

        self.new_task_data = {
            'id': 2,  # This is not used, but it's here to make the tests data complete
            'title': 'New Test Task',
            'description': 'New Test Description',
            'type': self.type.type,
            'status': self.status.status,
            'assigneeId': self.user.id,
            'creatorId': self.user.id,
            'projectId': self.project.id,
        }

        self.patch_data = {
            'title': 'Updated Test Task',
            'description': 'Updated Test Description',
            'type': self.type.type,
            'status': self.status.status,
            'assigneeId': self.user.id,
        }

        # Set up the tests client
        self.client = APIClient()

    def test_get_task(self):
        expected = {
            'id': self.task.id,
            'title': self.task.title,
            'description': self.task.description,
            'type': self.task.type_id,
            'status': self.task.status_id,
            'assigneeId': self.task.assignee_id,
            'projectId': self.task.project_id,
        }

        response = self.client.get(f'/api/tasks/{self.task.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_utils.compare_tasks(self, expected, response.data)

    def test_get_all_tasks(self):
        response = self.client.get('/api/tasks')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_nonexistent_task(self):
        response = self.client.get('/api/tasks/999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('sockets.utils.sockets_utils.send_task_create_event')
    def test_create_task(self, mock_send_task_create_event):
        response = self.client.post('/api/tasks', data=self.new_task_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_task = Task.objects.get(title='New Test Task')
        self.assertIsNotNone(new_task)
        test_utils.compare_tasks(self, self.new_task_data, new_task)
        mock_send_task_create_event.assert_called_with(self.project.id, new_task)

    def test_create_task_bad_request(self):
        self.new_task_data['title'] = ''

        response = self.client.post('/api/tasks', data=self.new_task_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('sockets.utils.sockets_utils.send_task_update_event')
    def test_update_task(self, mock_send_task_create_event):
        expected = {
            'id': self.task.id,
            'title': 'Updated Test Task',
            'description': 'Updated Test Description',
            'type': self.type.type,
            'status': self.status.status,
            'assignee_id': self.user.id,
            'project_id': self.project.id,
        }

        response = self.client.patch(f'/api/tasks/{self.task.id}', data=self.patch_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=self.task.id)
        mock_send_task_create_event.assert_called_with(self.project.id, updated_task)
        test_utils.compare_tasks(self, expected, updated_task)

    def test_update_bad_request(self):
        response = self.client.patch(f'/api/tasks/{self.task.id}', data={
            'title': '',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('sockets.utils.sockets_utils.send_task_delete_event')
    def test_delete_task(self, mock_send_task_create_event):
        response = self.client.delete(f'/api/tasks/{self.task.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        mock_send_task_create_event.assert_called_with(self.project.id, self.task.id)

    def test_delete_nonexistent_task(self):
        response = self.client.delete('/api/tasks/999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
