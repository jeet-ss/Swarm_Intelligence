import xml.etree.ElementTree as ET
import numpy as np

def XMLParser():
    xmlfile = './Sheet_05/graph.xml'
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
    children = root.getchildren()
    relevance = np.full(len(children), 1 / len(children))
    d_value = 4/5
    graph = {}
    nodes = []
    edges = {}
    for child in root:
        if(child.tag == 'node'):
            #print(child.tag, child.attrib['id'], child.attrib['name'])
            id = child.attrib['id']
            name = child.attrib['name']
            nodes.append(id)
            print('I found a node with id %s and name %s\n',id,name)
            ########
            #
            #####

        if(child.tag == 'edge'):
            id = child.attrib['id']
            source = child.attrib['source']
            target = child.attrib['target']
            print('I found a edge with id %s from %s to %s\n',id,source,target)
            ########
            #
            #####



if __name__ == "__main__":

	# calling main function
	XMLParser()
