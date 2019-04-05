import unittest
from operator import attrgetter

from gitlab_functions import get_gitlab
import collections
from datetime import datetime
import json

class TestGitlabProperties(unittest.TestCase):
    def test_commits(self):
        gl =  get_gitlab()
        TEST_GROUP = 434
        g = gl.groups.get(TEST_GROUP)
        print("getting projects")
        projects = sorted(g.projects.list(all=True),key=attrgetter('name'))
        print("got projects {}".format(len(projects)))
        commits_wanted = 100
        commits_returned = []
        commit_by_project = {}

        since_timestamp=datetime(2016,3,30).strftime("%Y-%m-%dT%H:%M:%SZ") # there's a bunch of garbage data in there before this.
        print("get sommits since: {}".format(since_timestamp))
        for p in projects:
            last_timestamp = None  # datetime.now().strftime("%Y-%m-$dT%H:%M:%SZ")
            last_commit = None
            project_commits = []
            while commits_wanted > len(commits_returned):
                if last_timestamp is None:
                    c= gl.projects.get(p.id).commits.list(all=True,since=since_timestamp)
                else:
                    c = gl.projects.get(p.id).commits.list(since=since_timestamp,until=last_timestamp)
                print("got commits {} for project {} {}".format(len(c),p.id,p.name))
                if len(c)>0:
                    last_timestamp = min([commit.created_at for commit in c])
                    if last_commit:
                        if last_commit.id == c[0].id:
                            break

                    last_commit = c[0]
                else:
                    print("no more commits in {}".format(p.name))
                    break
                print("last timestamp{}".format(last_timestamp))
                commits_returned.extend(c)
                print("total commits {}".format(len(commits_returned)))
                project_commits.extend(c)


        print("number of commits: {}".format(len(commits_returned)))
        author_list = [commit.author_name for commit in commits_returned]
        counter = collections.Counter(author_list)

        print("most commits by: {}".format(counter.most_common(50)))

