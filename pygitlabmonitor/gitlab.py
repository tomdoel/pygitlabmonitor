import os
import tempfile

import gitlab
import urllib

import PIL
import PIL.Image
import PIL.ImageTk

from pygitlabmonitor import settings

THUMBNAIL_SIZE = [40, 40]


class GitLab(object):
    def __init__(self):
        self._gl = gitlab.Gitlab(settings.SERVER, settings.TOKEN)
        self._gl.auth()

    def initialise_icons(self, project_cache):
        groups = self._gl.groups.list()
        temp_dir = tempfile.gettempdir()
        icon_filename = os.path.join(temp_dir, 'downloaded_icon')

        for group in groups:
            url = group.avatar_url
            if url:
                urllib.request.urlretrieve(url, icon_filename)
                pil_image = PIL.Image.open(icon_filename).convert("RGB")
                pil_image.thumbnail(THUMBNAIL_SIZE, PIL.Image.ANTIALIAS)
                icon = PIL.ImageTk.PhotoImage(pil_image)
            else:
                icon = None

            group_projects = group.projects.list(all=True)
            for project in group_projects:
                project_cache.add_icon(group.name, project.name, icon)

    def get_project_status(self, project_cache):
        projects = self._gl.projects.list(all=True)
        for project in projects:
            try:
                builds = project.builds.list()
                if builds:
                    pipelines = project.pipelines
                    if pipelines:
                        pipelines_list = pipelines.list()
                        latest_pipeline = pipelines_list[-1]
                        print("PROJECT:" + project.name + " : " + latest_pipeline.status)
                        commits = project.commits.list()
                        if commits:
                            last_commit = commits[0]
                            statuses = last_commit.statuses.list()
                            global_status = self._merge_status(statuses)
                            print(" - " + global_status)
                            project_cache.set_status(project.namespace.name, project.name, global_status)

            except Exception as e:
                print("Failed to get status for:" + project.name + ": " + str(e))

    @staticmethod
    def _merge_status(statuses):
        global_status = None
        if statuses:
            for status in statuses:
                current_status = status.status
                print("**" + current_status)

                if current_status == 'failed':
                    global_status = 'failed'
                    return global_status

                elif current_status == 'cancelled':
                    global_status = 'cancelled'

                elif current_status == 'success':
                    if (not global_status) or (global_status == 'skipped'):
                        global_status = 'success'

                elif current_status == 'pending':
                    if not (global_status == 'cancelled' or global_status == 'running'):
                        global_status = 'pending'

                elif current_status == 'created':
                    if not (global_status == 'cancelled' or global_status == 'running'):
                        global_status = 'created'

                elif current_status == 'running':
                    if not (global_status == 'cancelled'):
                        global_status = 'running'

                elif current_status == 'skipped':
                    if not global_status:
                        global_status = 'skipped'

                else:
                    global_status = 'UNKNOWN'
                    return global_status

        if global_status:
            return global_status
        else:
            return "unknown"
