__author__ = 'Yijun Pan'

import csv
from graph_tool import *
from graph_tool import topology
import glob
from lxml import etree as ET


def read_blueprint_index(filename):
    with open(filename, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        blueprint_index = {}
        for idx, row in enumerate(reader):
            if idx == 0:
                print row
            else:
                blueprint_index[row[1]] = idx

    return blueprint_index


def read_dependency(filename, blueprint_index, graph):
    myparser = ET.XMLParser(recover=True)
    tree = ET.parse(filename, myparser)
    root = tree.getroot()
    for child in root.iterchildren(tag="blueprint"):
        dependencies = child.find('dependencies')
        if dependencies.text == 'None':
            continue
        name_src = child.find('name').text
        index_src = blueprint_index.get(name_src)
        if index_src is None:
            continue

        for name_tgt in dependencies.itertext():
            index_tgt = blueprint_index.get(name_tgt)

            if index_tgt is None:
                continue
            else:
                graph.add_edge(graph.vertex(index_tgt), graph.vertex(index_src))


def build_dependency_tree(index_filename, dependency_filename, output_file="dep_tree"):
    graph = Graph()
    # Index start with 1
    blueprint_index = read_blueprint_index(index_filename)

    # All dependency file should be like filename_*.xml
    filename_pattern = dependency_filename+"_*.xml"
    #filename_pattern = "blueprints.xml"
    filenames = glob.glob(filename_pattern)

    print filenames

    print len(blueprint_index)
    key, value = max(blueprint_index.iteritems(), key=lambda x:x[1])

    print value

    graph.add_vertex(len(blueprint_index)+1)

    for filename in filenames:
        read_dependency(filename, blueprint_index, graph)

    in_degree = ['in_degree']
    out_degree = ['out_degree']

    for i in range(1, len(blueprint_index)+1):
        in_degree.append(graph.vertex(i).in_degree())
        out_degree.append(graph.vertex(i).out_degree())

    in_degree_file = output_file+"_in.csv"
    out_degree_file = output_file+"_out.csv"

    with open(in_degree_file, 'wb') as fp:
            writer = csv.writer(fp)
            for i in range(0, len(blueprint_index)+1):
                writer.writerow([in_degree[i]])
    fp.close()

    with open(out_degree_file, 'wb') as fp:
            writer = csv.writer(fp)
            for i in range(0, len(blueprint_index)+1):
                writer.writerow([out_degree[i]])
    fp.close()


def find_connected_component_label(index_filename, dependency_filename, output_file="dep_tree_cc_label"):
    graph = Graph()
    # Index start with 1
    blueprint_index = read_blueprint_index(index_filename)

    # All dependency file should be like filename_*.xml
    filename_pattern = dependency_filename+"_*.xml"
    #filename_pattern = "blueprints.xml"
    filenames = glob.glob(filename_pattern)

    print filenames

    print len(blueprint_index)
    key, value = max(blueprint_index.iteritems(), key=lambda x:x[1])

    print value

    graph.add_vertex(len(blueprint_index)+1)

    for filename in filenames:
        read_dependency(filename, blueprint_index, graph)

    cc_label = ['cc_label']
    cc_hist = ['cc_hist']

    comp, hist = topology.label_components(graph, directed=False)


    for i in range(1, len(blueprint_index)+1):
        cc_label.append(comp.a[i])
        cc_hist.append(hist[comp.a[i]])


    output_file += ".csv"
    with open(output_file, 'wb') as fp:
        writer = csv.writer(fp)
        for i in range(0, len(blueprint_index)+1):
            writer.writerow([cc_label[i], cc_hist[i]])

    fp.close()











