from core.models.project import Project


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
