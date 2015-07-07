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

    @staticmethod
    def __prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="/t")

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


    def write_to_file(self, output_file="output.xml", pretty=False):

        if not self.__dataset:
            print "Dataset is empty. Nothing is written out."
            return

        # TODO: Currently the writer only supports single level attributes.
        root = ET.Element(self.__name)

        # Add a simple comment if necessary
        if self.__comment is not None:
            root.append(ET.Comment(self.__comment))

        # Use index as element tag is a bad idea
        for idx, data in enumerate(self.__dataset):

            data_element = ET.SubElement(root, "blueprint")

            for attribute in data.__dict__.keys():
                value = getattr(data, attribute)
                attr_element = ET.SubElement(data_element, attribute)

                if not isinstance(value, list):
                    attr_element.text = str(value)
                else:
                    for i, v in enumerate(value):
                        sub_elem = ET.SubElement(attr_element, "dependency")
                        sub_elem.text = str(v)

        # Use pretty print carefullyÅ
        if pretty:
            self.indent(root)

        tree = ET.ElementTree(root)
        tree.write(output_file)



