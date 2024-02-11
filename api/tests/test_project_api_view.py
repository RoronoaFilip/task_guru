from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

import api.tests.utils as test_utils
from core.models.project import Project


class ProjectApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Project.objects.create(name='Test Project', description='Test Description', creator=self.user)

    def test_get_single_project(self):
        response = self.client.get(f'/api/projects/{self.project.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_utils.compare_projects(self, response.data, self.project)

    def test_get_all_projects(self):
        response = self.client.get('/api/projects')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_project(self):
        data = {'name': 'New Project', 'description': 'New Description', 'creator_id': self.user.id}

        response = self.client.post('/api/projects', data)

        data['id'] = 2
        data['creator'] = data['creator_id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_utils.compare_projects(self, response.data, data)

    def test_patch_project(self):
        data = {'description': 'Updated Description'}

        response = self.client.patch(f'/api/projects/{self.project.id}', data)

        expected = {'id': self.project.id, 'name': self.project.name, 'description': data['description'],
                    'creator': self.project.creator.id}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_utils.compare_projects(self, response.data, expected)

    def test_delete_project(self):
        response = self.client.delete(f'/api/projects/{self.project.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_invalid_project_id(self):
        response = self.client.get('/api/projects/999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
