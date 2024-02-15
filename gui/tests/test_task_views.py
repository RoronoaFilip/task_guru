from django.test import TestCase, Client

from core.models.task import Task
from core.tests import utils as test_utils


class ProjectGuiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = test_utils.create_user('testuser', 'testpassword')
        self.user_2 = test_utils.create_user('testuser2', 'testpassword')

        self.project = test_utils.create_project('Test Project', 'Test Description', self.user, 'github_username',
                                                 'github_name')
        self.type = test_utils.create_type('BUG')
        self.type_2 = test_utils.create_type('STATUS')
        self.status = test_utils.create_status('OPEN')
        self.status_2 = test_utils.create_status('DONE')
        self.task_1 = test_utils.create_task('Test Task 1', 'Test Task Description 1', self.project, self.user,
                                             self.status, self.type)
        self.task_2 = test_utils.create_task('Test Task 2', 'Test Task Description 2', self.project, self.user,
                                             self.status_2, self.type)
        self.task_3 = test_utils.create_task('Test Task 3', 'Test Task Description 3', self.project, self.user,
                                             self.status, self.type_2, self.user_2)

    def test_get_task(self):
        self.client.force_login(self.user)

        response = self.client.get('/tasks/1/card')

        self.assertEqual(response.status_code, 200)
        self._assert_task_rendered(response, self.task_1, exclude_description=True)
        self.assertTemplateUsed(response, 'tasks/task.html')

    def test_get_task_page(self):
        self.client.force_login(self.user)

        response = self.client.get('/tasks/2')

        self.assertEqual(response.status_code, 200)
        self._assert_task_rendered(response, self.task_2)
        self.assertTemplateUsed(response, 'tasks/task_page.html')

    def test_get_project_create_form(self):
        self.client.force_login(self.user)

        response = self.client.get(f'/tasks/{self.project.id}/create')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Task')
        self._assert_task_form_fields(response)
        self.assertTemplateUsed(response, 'form.html')

    def test_get_project_update_form(self):
        self.client.force_login(self.user)

        response = self.client.get('/tasks/3/update')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Task')
        self._assert_task_form_fields(response)
        self._assert_task_rendered(response, self.task_3)
        self.assertTemplateUsed(response, 'form.html')

    def test_post_task_create_form(self):
        self.client.force_login(self.user)

        response = self.client.post(f'/tasks/{self.project.id}/create', {
            'title': 'New Task',
            'description': 'New Description',
            'type': self.type_2.id,
            'status': self.status_2.id,
            'assignee': self.user_2.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/projects/{self.project.id}')

        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.title, 'New Task')
        self.assertEqual(new_task.description, 'New Description')
        self.assertEqual(new_task.type, self.type_2)
        self.assertEqual(new_task.status, self.status_2)
        self.assertEqual(new_task.assignee, self.user_2)
        self.assertEqual(new_task.creator, self.user)
        self.assertEqual(new_task.project, self.project)

    def test_post_task_update_form(self):
        self.client.force_login(self.user)

        response = self.client.post(f'/tasks/{self.task_1.id}/update', {
            'title': 'Updated Task',
            'description': 'Updated Task Description',
            'type': self.type_2.id,
            'status': self.status_2.id,
            'assignee': self.user_2.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/projects/{self.project.id}')

        updated_task = Task.objects.get(id=self.task_1.id)
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertEqual(updated_task.description, 'Updated Task Description')
        self.assertEqual(updated_task.type, self.type_2)
        self.assertEqual(updated_task.status, self.status_2)
        self.assertEqual(updated_task.assignee, self.user_2)

    def _assert_task_form_fields(self, response):
        self.assertContains(response, 'Title')
        self.assertContains(response, 'Description')
        self.assertContains(response, 'Type')
        self.assertContains(response, 'Status')
        self.assertContains(response, 'Assignee')

    def _assert_task_rendered(self, response, task, exclude_description=False):
        self.assertContains(response, task.title)
        self.assertContains(response, task.type)
        self.assertContains(response, task.status)
        self.assertContains(response, task.assignee)
        if not exclude_description:
            self.assertContains(response, task.description)
