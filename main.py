__author__ = 'Yijun Pan'

from launchpadCrawler import LaunchpadCrawler
import buildDepTrees

def get_bug_data(crawler):
    attributes=['date_created', 'date_assigned', 'date_closed',
                                       'bug_target_name',
                                       'web_link',
                                       'status', 'is_complete', 'importance',
                                       'owner', 'assignee']
    project_names = ['openstack']
    output_file = '100_bugs.xml'

    crawler.crawl_project_bugs(project_names=project_names, attributes=attributes,
                               output_file=output_file, output_type='xml', bug_amount=100)

def get_blueprint_dependencies(crawler):
    attributes=['dependencies']
    project_names = ['openstack']
    output_file = 'blueprints.xml'

    crawler.crawl_project_blueprints(project_names=project_names, attributes=attributes,
                                     output_file=output_file, output_type='xml', amount=0,
                                     write_through=True, trunk_size=1000, pretty_print=False)


def get_blueprint_whiteboard(crawler):
    attributes=['whiteboard']
    project_names = ['openstack']
    output_file = 'blueprints_whiteboard.xml'

    crawler.crawl_project_blueprints(project_names=project_names, attributes=attributes,
                                     output_file=output_file, output_type='xml', amount=0,
                                     write_through=True, trunk_size=1000, pretty_print=False)



def main():
    #crawler = LaunchpadCrawler('just testing', 'production', 'cache')
    #get_blueprint_whiteboard(crawler)
    #get_bug_data(crawler)
    #get_blueprint_dependencies(crawler)
    index_filename = "blueprint_id.csv"
    dependency_filename = "blueprints"
    #buildDepTrees.build_dependency_tree(index_filename, dependency_filename)
    buildDepTrees.find_connected_component_label(index_filename, dependency_filename)

if __name__ == "__main__":
    main()
