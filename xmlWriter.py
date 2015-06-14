__author__ = 'Yijun Pan'

import xml.etree.cElementTree as ET
from xml.dom import minidom

class xmlWriter:
    __dataset = None
    __name = None
    __comment = None

    def __init__(self, dataset=None, name="data", comment=None):
        self.__dataset = dataset
        self.__name = name
        self.__comment = comment

    def add_comment(self, comment=None):
        # TODO: Add support for multiple comments
        if comment is not None:
            self.__comment = comment

    def __prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def write_to_file(self, output_file="output.xml", pretty=True):

        if not self.__dataset:
            print "Dataset is empty. Nothing is written out."
            return

        # TODO: Currently the writer only supports single level attributes.
        root = ET.Element(self.__name)

        # Add a simple comment if necessary
        if self.__comment is not None:
            root.append(ET.Comment(self.__comment))

        for idx, data in enumerate(self.__dataset):

            data_element = ET.SubElement(root, str(idx))

            for attribute in data.__dict__.keys():
                value = getattr(data, attribute)
                attr_element = ET.SubElement(data_element, attribute)
                attr_element.text = str(value)

        if pretty:
            root = self.__prettify(root)

        tree = ET.ElementTree(root)
        tree.write(output_file)



