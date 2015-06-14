__author__ = 'Yijun Pan'

from launchpadCrawler import LaunchpadCrawler


def get_bug_data(crawler):
    attributes=['date_created', 'date_assigned', 'date_closed',
                                       'bug_target_name',
                                       'status', 'is_complete',
                                       'owner', 'assignee']
    project_names = ['openstack']
    output_file = 'openstack_bugs.xml'

    crawler.crawl_project_bugs(project_names=project_names, attributes=attributes,
                               output_file=output_file, output_type='xml')



def main():
    crawler = LaunchpadCrawler('just testing', 'production', 'cache')
    get_bug_data(crawler)

if __name__ == "__main__":
    main()
