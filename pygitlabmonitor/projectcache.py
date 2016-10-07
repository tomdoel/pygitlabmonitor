
class ProjectStatus:
    def __init__(self, name):
        self.name = name
        self.icon = None
        self.status = None

    def add_icon(self, icon):
        self.icon = icon

    def set_status(self, status):
        self.status = status


class ProjectStatusDictionary(object):
    def __init__(self):
        self.projects = dict()

    def get_project(self, project):
        if project not in self.projects:
            self.projects[project] = ProjectStatus(project)
        return self.projects[project]


class ProjectCache(object):
    def __init__(self):
        self.namespaces = dict()

    def add_icon(self, namespace, project, icon):
        self.get_project(namespace, project).add_icon(icon)

    def set_status(self, namespace, project, status):
        self.get_project(namespace, project).set_status(status)

    def get_project(self, namespace, project):
        if namespace not in self.namespaces:
            self.namespaces[namespace] = ProjectStatusDictionary()
        return self.namespaces[namespace].get_project(project)

    def get_list_of_statuses(self):
        status_list = []
        for namespace in self.namespaces.values():
            for project in namespace.projects.values():
                status_list.append(project)
        return status_list
