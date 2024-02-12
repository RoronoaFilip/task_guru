from django.test import TestCase

from core.serializers import ProjectSerializer, TaskSerializer
from core.test import utils


class SerializersTest(TestCase):
    def setUp(self):
        self.user = utils.create_user('testuser', 'testpassword')
        self.project = utils.create_project('Test Project', 'Test Description', self.user, 'github_username',
                                            'github_name')
        self.type = utils.create_type('BUG')
        self.status = utils.create_status('OPEN')
        self.task = utils.create_task('Test Task', 'Test Task Description', self.project, self.user, self.status,
                                      self.type)

    def test_create_project(self):
        create_data = {
            'name': 'Test Create Project',
            'description': 'Test Create Description',
            'creator': 1,
            'github_username': 'github_username create',
            'github_name': 'github_name create'
        }
        expected = {**create_data, 'creator': self.project.creator}
        serializer = ProjectSerializer(data=create_data)

        self.assertTrue(serializer.is_valid())

        actual = serializer.save()
        self.assertProject(actual, expected)

    def test_create_project_not_valid(self):
        create_data = {
            'name': '',
            'description': 'Test Create Description',
            'creator': self.user,
            'github_username': 'github_username create',
            'github_name': 'github_name create'
        }
        serializer = ProjectSerializer(data=create_data)

        self.assertFalse(serializer.is_valid())

    def test_update_project(self):
        patch_data = {
            'name': 'Test Update Project',
            'description': 'Test Update Description',
            'github_username': 'github_username update',
            'github_name': 'github_name update'
        }
        expected = {**patch_data, 'creator': self.project.creator}

        serializer = ProjectSerializer(self.project, data=patch_data, partial=True)

        self.assertTrue(serializer.is_valid())
        actual = serializer.save()
        self.assertProject(actual, expected)

    def test_update_project_not_valid(self):
        patch_data = {
            'name': '',
            'description': 'Test Update Description',
            'github_username': 'github_username update',
            'github_name': 'github_name update'
        }
        serializer = ProjectSerializer(self.project, data=patch_data, partial=True)

        self.assertFalse(serializer.is_valid())

    def test_create_task(self):
        create_data = {
            'title': 'Test Create Task',
            'description': 'Test Create Description',
            'type': self.type.id,
            'status': self.status.id,
            'creator': 1,
            'project': self.project.id
        }
        expected = {
            **create_data,
            'assignee': None,
            'project': self.project,
            'creator': self.user,
            'status': self.status,
            'type': self.type
        }

        serializer = TaskSerializer(data=create_data)

        self.assertTrue(serializer.is_valid())
        actual = serializer.save()
        self.assertTask(actual, expected)

    def test_create_task_not_valid(self):
        create_data = {
            'title': 'Test Create Task',
            'description': 'Test Create Description',
            'type': None,
            'status': self.status.id,
            'assignee': self.user.id,
            'creator': self.user.id,
            'project': self.project.id
        }

        serializer = TaskSerializer(data=create_data)

        self.assertFalse(serializer.is_valid())

    def test_update_task(self):
        patch_data = {
            'title': 'Test Update Task',
            'description': 'Test Update Description',
            'type': self.type.id,
            'status': self.status.id,
            'assignee': None,
            'creator': self.user.id,
            'project': self.project.id
        }
        expected = {
            **patch_data,
            'assignee': None,
            'project': self.project,
            'creator': self.user,
            'status': self.status,
            'type': self.type
        }

        serializer = TaskSerializer(self.task, data=patch_data, partial=True)

        self.assertTrue(serializer.is_valid())
        actual = serializer.save()
        self.assertTask(actual, expected)

    def test_update_task_not_valid(self):
        patch_data = {
            'title': 'Test Update Task',
            'description': 'Test Update Description',
            'type': self.type.id,
            'status': self.status.id,
            'assignee': self.user.id,
            'creator': self.user.id,
            'project': None
        }

        serializer = TaskSerializer(self.task, data=patch_data, partial=True)

        self.assertFalse(serializer.is_valid())

    def assertProject(self, actual, expected):
        """Asserts that the actual project matches the expected project."""
        self.assertEqual(actual.name, expected['name'])
        self.assertEqual(actual.description, expected['description'])
        self.assertEqual(actual.creator, expected['creator'])
        self.assertEqual(actual.github_username, expected['github_username'])
        self.assertEqual(actual.github_name, expected['github_name'])

    def assertTask(self, actual, expected):
        """Asserts that the actual task matches the expected task."""
        self.assertEqual(actual.title, expected['title'])
        self.assertEqual(actual.description, expected['description'])
        self.assertEqual(actual.project, expected['project'])
        self.assertEqual(actual.creator, expected['creator'])
        self.assertEqual(actual.status, expected['status'])
        self.assertEqual(actual.type, expected['type'])
        self.assertEqual(actual.assignee, expected['assignee'])
