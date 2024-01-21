from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from core.models.task import Task, Type, Status
from core.models.project import Project

class TaskViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create some test data
        self.type = Type.objects.create(type='Test Type')
        self.status = Status.objects.create(status='OPEN')
        self.project = Project.objects.create(name='Test Project', description='Test Description', creator=self.user)

        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'type': self.type,
            'status': self.status,
            'assignee': self.user,
            'creator': self.user,
            'project': self.project,
        }
        self.task = Task.objects.create(**self.task_data)

        # Set up the test client
        self.client = APIClient()

    def test_get_task(self):
        response = self.client.get(f'/api/tasks/{self.task.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_tasks(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_task(self):
        response = self.client.get('/api/tasks/999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task(self):
        # Set up test data for creating a new task
        new_task_data = {
            'title': 'New Test Task',
            'description': 'New Test Description',
            'type': self.type.type,
            'assignee_id': self.user.id,
            'creator_id': self.user.id,
            'project_id': self.project.id,
        }

        response = self.client.post('/api/tasks', data=new_task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_task = Task.objects.get(title='New Test Task')
        self.assertIsNotNone(new_task)

    def test_update_task(self):
        updated_data = {
            'title': 'Updated Test Task',
            'description': 'Updated Test Description',
            'type': self.type.type,
            'status': self.status.status,
            'assignee_id': self.user.id,
        }

        response = self.client.patch(f'/api/tasks/{self.task.id}', data=updated_data),
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, 'Updated Test Task')

    def test_delete_task(self):
        response = self.client.delete(f'/api/tasks/{self.task.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)
