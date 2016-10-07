import tkinter

from pygitlabmonitor.gitlab import GitLab
from pygitlabmonitor.monitorframe import MonitorFrame
from pygitlabmonitor.projectcache import ProjectCache


class Monitor:

    def __init__(self):
        self._gitlab = GitLab()

        root = tkinter.Tk()
        root.title("cmiclab status")

        project_cache = ProjectCache()

        self._gitlab.initialise_icons(project_cache)
        self._gitlab.get_project_status(project_cache)

        MonitorFrame(root, project_cache)
        root.mainloop()

