__author__ = 'Shawn'

import re
import xml.etree.cElementTree as ET
import dataStruct
import xmlWriter

def extract_review_urls(whiteboard):
    # Whiteboard messages are coded in unicode
    review_re = re.compile(ur'https://review.openstack.org/[0-9]{1,}', re.UNICODE)
    result = review_re.findall(whiteboard)
    return result

def extract_all_reviews(whiteboards_xml, output_file):
    # TODO: move all the io operations to another class
    blueprints_data = []

    for whiteboard_xml in whiteboards_xml:
        tree = ET.parse(whiteboard_xml)
        root = tree.getroot()
        for child in root.iterchildren(tag="blueprint"):
            blueprint_data = dataStruct.Blueprint(child.find("name").text)
            whiteboard = child.find('whiteboard')

            review_urls = extract_review_urls(whiteboard.text)
            if not review_urls:
                setattr(blueprint_data, "review_urls", None)
            else:
                urls = []
                for review_url in review_urls:
                    urls.append(review_url)
                    setattr(blueprint_data, "review_urls", urls)

    # LoL, super huge file
    writer = xmlWriter(blueprints_data, "blueprints", "All blueprints belong to project OpenStack")
    writer.write_to_file(output_file, pretty=False)
