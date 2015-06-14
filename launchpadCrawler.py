__author__ = 'Yijun Pan'

from launchpadlib.launchpad import Launchpad
from xmlWriter import xmlWriter
from csvWriter import csvWriter

import os
import sys


class Project:
    name = None

    def __init__(self, name="undefined"):
        self.name = name

    def list_attributes(self):
        print self.__dict__.keys()


class Bug:
    title = None

    def __init__(self, title="undefined"):
        self.title = title

    def list_attributes(self):
        print self.__dict__.keys()


class LaunchpadCrawler:

    # Directory to store files from Launchpad
    __cachedir = ""
    __launchpad = None

    def __set_cache_dir(self, cachedir):
        self.__cachedir = cachedir
        if not os.path.isdir(self.__cachedir):
                os.makedirs(self.__cachedir)

    def set_authorization(self, application=None, server=None):

        if application is not None and server is not None:
            self.launchpad = Launchpad.login_with(application, server, self.__cachedir,
                                                  credential_save_failed=self.__no_credential)
        else:
            self.launchpad = Launchpad.login_anonymously('just testing', 'production', self.__cachedir)

    @staticmethod
    def __no_credential(self):
        print "Can't proceed without Launchpad credential."
        sys.exit()

    def __init__(self):
        self.__set_cache_dir("cache")
        self.set_authorization()

    def __init__(self, application=None, server=None, cachedir="cache"):
        self.__set_cache_dir(cachedir)
        self.set_authorization(application, server)

    # Get the bug info
    def crawl_project_bugs(self, project_names=[],
                           attributes=['date_created', 'date_assigned', 'date_closed',
                                       'bug_target_name',
                                       'status', 'is_complete',
                                       'owner', 'assignee'],
                           output_type="print",
                           output_file="output_bugs.xml"):

        for name in project_names:
            project = self.launchpad.projects(name)

            bugs = project.searchTasks(status=['New', 'Incomplete', 'Triaged', 'Opinion', 'Expired',
                                               'Invalid', 'Won\'t Fix', 'Confirmed', 'In Progress',
                                               'Fix Committed', 'Fix Released'])

            bugs_data = []

            print bugs.total_size + "bugs found."

            for bug in bugs:

                bug_data = Bug(bug.title)

                for attribute in attributes:
                    # Creator of the bug event
                    if attribute == 'owner':
                        owner = bug.owner
                        bug.owner_name = owner.name
                        bug.owner_link = owner.web_link

                    elif attribute == "asignee":
                        assignee = bug.assignee
                        bug.assignee_name = assignee.name
                        bug.assignee_link = assignee.web_link

                    else:
                        value = getattr(bug, attribute)
                        setattr(bug_data, attribute, value)

                bugs_data.append(bug_data)

            # write or print out bugs
            if output_type == "print":
                for bug_data in bugs_data:
                    print bug_data.__dict__
            elif output_file == "xml":
                writer = xmlWriter(bugs_data, "bugs", "All bugs belong to project OpenStack")
                writer.write_to_file(output_file, pretty=True)

            elif output_type == "csv":
                writer = csvWriter(bugs_data)
                writer.write_to_file(output_file, delimiter=',')
            else:
                print "Unsupported output format."




