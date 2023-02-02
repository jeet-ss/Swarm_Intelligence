###################################
#
# In this problem, the analysis of social networks is considered.
#
# The following graph, which is well known in the scientific community, describes by means of an
# edge which two users regularly exchange emails with each other. Because of its shape, the graph is 
# called Kite graph.
#
# We now want to look at how “central” a user is in a network and how this can be measured in the
# context of our question about the measurability of emergence. Three measures are widely used,
# they are called indicators of centrality.
#
###################################
import numpy as np
import parser
import networkx as nx


class KiteGraph():
    def __init__(self):
        pass
    def degree_C(self, G):
        #
        return nx.degree_centrality(G)

    def betweeness_C(self, G):
        #
        return nx.betweenness_centrality(G, k=None, normalized=True, 
                            weight=None, endpoints=False, seed=None)

    def closeness_C(self, G):
        #
        return nx.closeness_centrality(G, u=None, distance='distance', wf_improved=False)

    def print(self, C_d, C_b, C_c):
        #
        #print(C_d, '\n', C_b, '\n', C_c)
        for i in range(len(C_d)):
            print('\n', C_d.get(i) ,C_b.get(i) , C_c.get(i) )



if __name__ == "__main__" :
    xmlfile = './Sheet_05/kite.xml'
    root = parser.read_xml(xmlfile)
    nodes = parser.extract_nodes(root)
    edges = parser.extract_edges(root)
    adjacency_matrix = parser.get_adjacency_matrix(nodes, edges)
    graph = parser.adjacency_matrix_to_graph(adjacency_matrix)
    #
    kite = KiteGraph()
    C_d = kite.degree_C(graph)
    C_b = kite.betweeness_C(graph)
    C_c = kite.closeness_C(graph)
    kite.print(C_d, C_b, C_c)

