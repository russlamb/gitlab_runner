import os
from operator import attrgetter

import gitlab
import logging


class NoApiKeyException(Exception):
    """This exception is thrown when there is no API key set in the system environment variables"""

    def __init__(self, message, environment_variable=None):
        super().__init__(message)
        self.environment_variable = environment_variable


def is_api_key_set():
    """This function logs whether or not the api key is present"""
    api_key = os.environ.get("GITLAB_API")
    print("api_key is set?: {}".format(True if api_key else False))
    logging.info("api_key is set?: {}".format(True if api_key else False))


def get_gitlab():
    """This function returns a gitlab API object

    See https://python-gitlab.readthedocs.io/en/stable/ for more info"""
    os.environ['NO_PROXY'] = 'gitlab'
    api_key = os.environ.get("GITLAB_API")
    if api_key is None:
        raise NoApiKeyException("Environment Variable for API key not set: ".format("GITLAB_API"), "GITLAB_API")

    gl = gitlab.Gitlab('https://gitlab', private_token=api_key, ssl_verify=False)  # 12/3/18 added to avoid SSL error
    return gl


def get_file(project_id, file_path, branch):
    """Get the Unicode content of the file and return contents as a string"""
    gl = get_gitlab()
    p = gl.projects.get(project_id)

    content = p.files.get(file_path, branch)

    return content.decode().decode('utf-8-sig')  # gitlab stores files as Base64 with text encoded in UTF-8 (Signed).


def print_groups():
    """Print the names of groups the current user has access to see

    This is mainly used for testing"""
    gl = get_gitlab()
    for g in gl.groups.list():
        print("group id: {}, name: {}".format(g.id, g.name))


def print_projects(group_id):
    """Show all projects (repos) for group

    This is mainly used for testing"""
    gl = get_gitlab()

    # [print(g) for g in gl.groups.list(all=True)]  # this prints all authorized groups.
    g = gl.groups.get(group_id)  # 434 is target group.
    projects = []
    print('group id: {}'.format(group_id))
    for p in sorted(g.projects.list(all=True), key=attrgetter('name')):  # uses name attribute to sort project object
        print("project: {}, id: {}".format(p.name, p.id))
        projects.append(p)
    return projects


def print_project_branches(project_id):
    """Show branches in project (repo)

    This is mainly used for testing"""
    gl = get_gitlab()
    p = gl.projects.get(project_id)
    branches = []
    for f in p.branches.list(all=True):
        print("file: {}".format(f))
        branches.append(f)
    return branches
