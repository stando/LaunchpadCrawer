__author__ = 'Yijun Pan'

from launchpadlib.launchpad import Launchpad
from xmlWriter import xmlWriter
from csvWriter import csvWriter

import os
import sys
import dataStruct

# TODO: Make launchpadCrawler faster with multiprocessing
# TODO: Add a routine to check reviews

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
                                                  credential_save_failed=self.__no_credential, version='devel')
        else:
            self.launchpad = Launchpad.login_anonymously('just testing', 'production', self.__cachedir, version='devel')

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
                                       'web_link',
                                       'bug_target_name',
                                       'status', 'is_complete', 'importance'
                                       'owner', 'assignee'],
                           output_type='print',
                           output_file="output_bugs.xml",
                           bug_amount=100,
                           write_through=False,
                           trunk_size=1000,
                           pretty_print=False):

        for name in project_names:
            project = self.launchpad.projects(name)

            bugs = project.searchTasks(status=['New', 'Incomplete', 'Triaged', 'Opinion', 'Expired',
                                               'Invalid', 'Won\'t Fix', 'Confirmed', 'In Progress',
                                               'Fix Committed', 'Fix Released'])

            bugs_data = []

            print str(bugs.total_size) + " bugs found."

            entry_count = 0
            file_count = 0

            for idx, bug in enumerate(bugs):

                if bug_amount > 0:
                    if idx >= bug_amount:
                        break

                entry_count += 1
                bug_data = Bug(bug.title)

                for attribute in attributes:
                    # Creator of the bug event
                    if attribute == 'owner':
                        # We should always have an owner
                        owner = bug.owner
                        setattr(bug_data, 'owner_name', owner.display_name)
                        setattr(bug_data, 'owner_link', owner.web_link)

                    elif attribute == "assignee":
                        # Sometimes we don't have an assignee
                        assignee = bug.assignee
                        if not assignee:
                            setattr(bug_data, 'assignee_name', None)
                            setattr(bug_data, 'assignee_link', None)
                        else:
                            setattr(bug_data, 'assignee_name', assignee.display_name)
                            setattr(bug_data, 'assignee_link', assignee.web_link)

                    else:
                        value = getattr(bug, attribute)
                        setattr(bug_data, attribute, value)

                bugs_data.append(bug_data)

                # Save large size data into multiple files if necessary
                if entry_count == trunk_size and write_through:

                    entry_count = 0
                    file_count += 1

                    out_file_name, out_file_ext = os.path.splitext(output_file)
                    out_file = out_file_name + '_' + str(file_count) + out_file_ext

                    if output_type == "print":
                        for bug_data in bugs_data:
                            print bug_data.__dict__

                    elif output_type == "xml":
                        writer = xmlWriter(bugs_data, "bugs", "All bugs belong to project OpenStack")
                        writer.write_to_file(out_file, pretty=pretty_print)

                    elif output_type == "csv":
                        writer = csvWriter(bugs_data)
                        writer.write_to_file(out_file, delimiter=',')
                    else:
                        print "Unsupported output format"
                        sys.exit(-1)

                    bugs_data = []

            if not bug_data:
                return

            # write or print out bugs
            if output_type == "print":
                for bug_data in bugs_data:
                    print bug_data.__dict__

            elif output_type == "xml":
                writer = xmlWriter(bugs_data, "bugs", "All bugs belong to project OpenStack")
                writer.write_to_file(output_file, pretty=pretty_print)

            elif output_type == "csv":
                writer = csvWriter(bugs_data)
                writer.write_to_file(output_file, delimiter=',')
            else:
                print "Unsupported output format."


    # Get blueprint of projects
    def crawl_project_blueprints(self, project_names=[],
                                 attributes=['date_created', 'date_started', 'date_completed',
                                       'web_link',
                                       'title',
                                       'dependencies',
                                       'implementation_status', 'priority',
                                       'owner', 'assignee'],
                                 output_type='print',
                                 output_file="output_blueprints.xml",
                                 amount=100,
                                 write_through=False,
                                 trunk_size=10,
                                 pretty_print=False):

        for name in project_names:
            project = self.launchpad.projects(name)
            blueprints = project.all_specifications

            blueprints_data = []

            print str(blueprints.total_size) + " blueprints found."

            entry_count = 0
            trunk_count = 0

            for idx, blueprint in enumerate(blueprints):

                if amount > 0:
                    if idx >= amount:
                        break

                entry_count += 1
                blueprint_data = Blueprint(blueprint.name+"("+blueprint.target.name+")")

                for attribute in attributes:
                    # Creator of the bug event
                    if attribute == 'owner':
                        # We should always have an owner
                        owner = blueprint.owner
                        setattr(blueprint_data, 'owner_name', owner.display_name)
                        setattr(blueprint_data, 'owner_link', owner.web_link)

                    elif attribute == "assignee":
                        # Sometimes we don't have an assignee
                        assignee = blueprint.assignee
                        if not assignee:
                            setattr(blueprint_data, 'assignee_name', None)
                            setattr(blueprint_data, 'assignee_link', None)
                        else:
                            setattr(blueprint_data, 'assignee_name', assignee.display_name)
                            setattr(blueprint_data, 'assignee_link', assignee.web_link)
                    elif attribute == "dependencies":
                        dependencies = blueprint.dependencies
                        if not dependencies:
                            setattr(blueprint_data, 'dependencies', None)
                        else:
                            dep_names = []
                            for dep in dependencies:
                                dep_names.append(dep.name+"("+dep.target.name+")")
                            setattr(blueprint_data, 'dependencies', dep_names)
                    else:
                        value = getattr(blueprint, attribute)
                        setattr(blueprint_data, attribute, value)

                blueprints_data.append(blueprint_data)

                # Save large size data into multiple files if necessary
                if entry_count == trunk_size and write_through:

                    entry_count = 0
                    trunk_count += 1

                    out_file_name, out_file_ext = os.path.splitext(output_file)
                    out_file = out_file_name + '_' + str(trunk_count) + out_file_ext

                    if output_type == "print":
                        for bug_data in blueprints_data:
                            print bug_data.__dict__

                    elif output_type == "xml":
                        writer = xmlWriter(blueprints_data, "bugs", "All bugs belong to project OpenStack")
                        writer.write_to_file(out_file, pretty=pretty_print)

                    elif output_type == "csv":
                        writer = csvWriter(blueprints_data)
                        writer.write_to_file(out_file, delimiter=',')
                    else:
                        print "Unsupported output format"
                        sys.exit(-1)

                    blueprints_data = []

            if not blueprints_data:
                return

            # write or print out bugs
            if output_type == "print":
                for blueprint_data in blueprints_data:
                    print bug_data.__dict__

            elif output_type == "xml":
                writer = xmlWriter(blueprints_data, "blueprints", "All blueprints belong to project OpenStack")
                writer.write_to_file(output_file, pretty=pretty_print)

            elif output_type == "csv":
                writer = csvWriter(blueprints_data)
                writer.write_to_file(output_file, delimiter=',')
            else:
                print "Unsupported output format."









