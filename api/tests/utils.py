from core.models.project import Project
from core.models.task import Task


def compare_projects(self, project_1, project_2):
    if isinstance(project_1, Project) and isinstance(project_2, Project):
        _compare_projects_objects(self, project_1, project_2)
    elif isinstance(project_1, dict) and isinstance(project_2, dict):
        _compare_projects_both_dict(self, project_1, project_2)
    elif isinstance(project_1, dict):
        _compare_projects_first_dict(self, project_1, project_2)
    elif isinstance(project_2, dict):
        _compare_projects_first_dict(self, project_2, project_1)


def _compare_projects_first_dict(self, dict_project, project):
    self.assertEqual(dict_project['id'], project.id)
    self.assertEqual(dict_project['name'], project.name)
    self.assertEqual(dict_project['description'], project.description)
    self.assertEqual(dict_project['creator'], project.creator.id)


def _compare_projects_both_dict(self, dict_project_1, dict_project_2):
    self.assertEqual(dict_project_1['id'], dict_project_2['id'])
    self.assertEqual(dict_project_1['name'], dict_project_2['name'])
    self.assertEqual(dict_project_1['description'], dict_project_2['description'])
    self.assertEqual(dict_project_1['creator'], dict_project_2['creator'])


def _compare_projects_objects(self, project_1, project_2):
    self.assertEqual(project_1.id, project_2.id)
    self.assertEqual(project_1.name, project_2.name)
    self.assertEqual(project_1.description, project_2.description)
    self.assertEqual(project_1.creator.id, project_2.creator.id)


def compare_tasks(self, task_1, task_2):
    if isinstance(task_1, Task) and isinstance(task_2, Task):
        _compare_tasks_objects(self, task_1, task_2)
    elif isinstance(task_1, dict) and isinstance(task_2, dict):
        _compare_tasks_both_dict(self, task_1, task_2)
    elif isinstance(task_1, dict):
        _compare_tasks_first_dict(self, task_1, task_2)
    elif isinstance(task_2, dict):
        _compare_tasks_first_dict(self, task_2, task_1)


def _compare_tasks_first_dict(self, dict_task, task):
    self.assertEqual(dict_task['id'], task.id)
    self.assertEqual(dict_task['title'], task.title)
    self.assertEqual(dict_task['description'], task.description)
    self.assertEqual(dict_task['type'], task.type.type)
    self.assertEqual(dict_task['status'], task.status.status)
    self.assertEqual(dict_task['assignee_id'], task.assignee_id)
    self.assertEqual(dict_task['project_id'], task.project.id)


def _compare_tasks_both_dict(self, dict_task_1, dict_task_2):
    self.assertEqual(dict_task_1['id'], dict_task_2['id'])
    self.assertEqual(dict_task_1['title'], dict_task_2['title'])
    self.assertEqual(dict_task_1['description'], dict_task_2['description'])
    self.assertEqual(dict_task_1['type'], dict_task_2['type'])
    self.assertEqual(dict_task_1['status'], dict_task_2['status'])
    self.assertEqual(dict_task_1['assignee_id'], dict_task_2['assignee'])
    self.assertEqual(dict_task_1['project_id'], dict_task_2['project'])



def _compare_tasks_objects(self, task_1, task_2):
    self.assertEqual(task_1.id, task_2.id)
    self.assertEqual(task_1.title, task_2.title)
    self.assertEqual(task_1.description, task_2.description)
    self.assertEqual(task_1.type.type, task_2.type.type)
    self.assertEqual(task_1.status.status, task_2.status.status)
    self.assertEqual(task_1.assignee_id, task_2.assignee_id)
    self.assertEqual(task_1.project.id, task_2.project.id)
