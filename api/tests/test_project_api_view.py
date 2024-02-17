from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

import api.tests.utils as test_utils
import core.tests.utils as core_utils
from core.models.project import Project


class ProjectApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = core_utils.create_project('Test Project', 'Test Description', self.user,
                                                 'github_username', 'github_name')
        self.type = core_utils.create_type('BUG')
        self.status = core_utils.create_status('OPEN')
        self.task_1 = core_utils.create_task('Test Task 1', 'Test Task Description 1', self.project, self.user,
                                             self.status, self.type)

    def test_get_single_project(self):
        response = self.client.get(f'/api/projects/{self.project.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_utils.compare_projects(self, response.data, self.project)

    def test_get_all_projects(self):
        response = self.client.get('/api/projects')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_project(self):
        data = {'name': 'New Project', 'description': 'New Description', 'creatorId': self.user.id}

        response = self.client.post('/api/projects', data)

        data['id'] = 2
        data['creator'] = data['creatorId']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_utils.compare_projects(self, response.data, data)

    def test_post_project_bad_request(self):
        data = {'name': 'New Project', 'description': 'New Description'}

        response = self.client.post('/api/projects', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_project(self):
        data = {'description': 'Updated Description'}

        response = self.client.patch(f'/api/projects/{self.project.id}', data)

        expected = {'id': self.project.id, 'name': self.project.name, 'description': data['description'],
                    'creator': self.project.creator.id}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_utils.compare_projects(self, response.data, expected)

    def test_patch_project_bad_request(self):
        data = {'name': '', 'description': 'New Description'}

        response = self.client.patch(f'/api/projects/{self.project.id}', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project(self):
        response = self.client.delete(f'/api/projects/{self.project.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_invalid_project_id(self):
        response = self.client.get('/api/projects/999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_project_members(self):
        response = self.client.get(f'/api/projects/{self.project.id}/members')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.user.id)
        self.assertEqual(response.data[0]['username'], self.user.username)

    def test_add_project_tasks(self):
        response = self.client.get(f'/api/projects/{self.project.id}/tasks')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        test_utils.compare_tasks(self, response.data[0]['title'], self.task_1.title)
        test_utils.compare_tasks(self, response.data[0]['description'], self.task_1.description)
