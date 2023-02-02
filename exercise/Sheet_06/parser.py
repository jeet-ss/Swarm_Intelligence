import numpy as np

import xml.etree.ElementTree as ET

import networkx as nx

def read_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def extract_nodes(root):
    nodes = []
    for node in root.iter('node'):
        nodes.append(node.attrib['id'])
    return nodes

def extract_nodes_names(root):
    node_names = []
    for node in root.iter('node'):
        node_names.append(node.attrib['name'])
    return node_names

def extract_edges(root):
    edges = []
    for edge in root.iter('edge'):
        edges.append((edge.attrib['source'], edge.attrib['target']))
    return edges

def get_adjacency_matrix(nodes, edges):
    adjacency_matrix = np.zeros((len(nodes), len(nodes)))
    for edge in edges:
        adjacency_matrix[nodes.index(edge[0])][nodes.index(edge[1])] = 1
    return adjacency_matrix


def adjacency_matrix_to_graph(adjacency_matrix):
    return nx.Graph(adjacency_matrix)