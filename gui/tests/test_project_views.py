from django.test import TestCase, Client

from core.models.project import Project
from core.test import utils as test_utils


class ProjectGuiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = test_utils.create_user('testuser', 'testpassword')
        self.user_2 = test_utils.create_user('testuser2', 'testpassword')
        self.user_3 = test_utils.create_user('testuser3', 'testpassword')

        self.project = test_utils.create_project('Test Project', 'Test Description', self.user, 'github_username',
                                                 'github_name')
        self.type = test_utils.create_type('Test Type')
        self.status = test_utils.create_status('OPEN')
        self.task_1, self.task_2, self.task_3 = test_utils.create_tasks(self.project, self.user, self.status, self.type)

        self.project_2 = test_utils.create_project('Test Project 2', 'Test Description 2', self.user_2,
                                                   'github_username_2',
                                                   'github_name_2')

    def test_get_projects_ignores_projects_user_is_not_a_member_of(self):
        self.client.force_login(self.user)

        response = self.client.get('/projects')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)
        self.assertNotContains(response, self.project_2.name)
        self.assertTemplateUsed(response, 'projects/projects.html')

    def test_get_projects_shows_no_projects_if_user_is_not_a_member_of_any(self):
        self.client.force_login(self.user_3)

        response = self.client.get('/projects')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Project')
        self.assertNotContains(response, 'Test Project 2')
        self.assertTemplateUsed(response, 'projects/projects.html')

    def test_get_project(self):
        self.client.force_login(self.user)

        response = self.client.get('/projects/1')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)
        self.assertContains(response, self.task_1.title)
        self.assertContains(response, self.task_2.title)
        self.assertContains(response, self.task_3.title)
        self.assertContains(response, self.status.status)
        self.assertTemplateUsed(response, 'projects/project.html')

    def test_get_project_create_form(self):
        self.client.force_login(self.user)

        response = self.client.get('/projects/create')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Project')
        self._assert_project_form_fields(response)
        self.assertTemplateUsed(response, 'form.html')

    def test_get_project_update_form(self):
        self.client.force_login(self.user)

        response = self.client.get('/projects/1/update')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Project')
        self._assert_project_form_fields(response)
        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.user.username)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_project_create_form(self):
        self.client.force_login(self.user)

        response = self.client.post('/projects/create', {
            'name': 'New Project',
            'description': 'New Description',
            'members': [self.user_2.id],
            'github_username': 'github_username',
            'github_name': 'github_name'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/projects')

        new_project = Project.objects.get(name='New Project')
        self.assertEqual(new_project.description, 'New Description')
        self.assertEqual(new_project.creator, self.user)
        self.assertTrue(new_project.members.contains(self.user))
        self.assertTrue(new_project.members.contains(self.user_2))
        self.assertEqual(new_project.github_username, 'github_username')
        self.assertEqual(new_project.github_name, 'github_name')

    def test_post_project_update_form(self):
        self.client.force_login(self.user)

        response = self.client.post(f'/projects/{self.project.id}/update', {
            'name': 'Updated Project',
            'description': 'Updated Description',
            'members': [self.user_2.id, self.user_3.id],
            'github_username': 'github_username 3',
            'github_name': 'github_name 3'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/projects')

        updated_project = Project.objects.get(id=self.project.id)
        self.assertEqual(updated_project.name, 'Updated Project')
        self.assertEqual(updated_project.description, 'Updated Description')
        self.assertEqual(updated_project.creator, self.user)
        self.assertFalse(updated_project.members.contains(self.user))
        self.assertTrue(updated_project.members.contains(self.user_3))
        self.assertTrue(updated_project.members.contains(self.user_2))
        self.assertEqual(updated_project.github_username, 'github_username 3')
        self.assertEqual(updated_project.github_name, 'github_name 3')

    def _assert_project_form_fields(self, response):
        self.assertContains(response, 'Name')
        self.assertContains(response, 'Description')
        self.assertContains(response, 'Members')
        self.assertContains(response, 'Github username')
        self.assertContains(response, 'Github name')
