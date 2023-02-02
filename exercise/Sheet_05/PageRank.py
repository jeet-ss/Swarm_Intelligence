import numpy as np
import parser

class PageRank():
    def __init__(self, root, nodes, edges, adjacency_matrix):
        #
        self.root = root
        self.nodes = nodes
        self.edges = edges
        self.adjacency_matrix  = adjacency_matrix
        #
        self.d = (1 / 5)
        self.outdegree = self.calculate_outdegree()
        self.relevance = np.full(len(nodes), 1 / len(nodes))
        self.transition_Mat = self.calculate_M()
        self.const_vector = np.full(len(nodes), ((1-self.d)/len(nodes)))
        #
        print(len(nodes), len(edges), adjacency_matrix.shape, self.relevance.shape)

    def calculate_outdegree(self):
        mat = np.sum(self.adjacency_matrix, axis=1)
        # TODO: how to init if sink
        mat_new = [(len(self.nodes)-1) if x==0 else x for x in mat]
        return mat_new


    def calculate_M(self):
        m = np.asarray(self.adjacency_matrix)
        for i in range(len(self.nodes)):
            if self.outdegree[i] != 0:
                m[:, i] = m[:, i]/self.outdegree[i]
            else:  # if no outbound nodes divide equally among all
                m[:, i] = m[:, i]/len(self.nodes)
        return m

    def iterations_pr(self):
        i_counter = 0
        #
        while i_counter < 100000:
            #
            i_counter += 1
            # set new relevance
            relevance_temp = self.const_vector +  self.d*np.matmul(self.transition_Mat, self.relevance)
            
            # termination criterion
            #if (np.sum(np.abs(relevance_temp) - np.abs(self.relevance))) < np.finfo(float).eps :
            self.relevance = relevance_temp
        #
        print(self.relevance, "\n max is: ", np.max(self.relevance), "of node: ", np.argmax(self.relevance))

    def itr_formula(self):
        i_counter = 0
        #val = ((1-self.d)/len(self.nodes)) 
        while i_counter < 10000:
            i_counter += 1
            #
            for idx, node in enumerate(self.nodes):
                relevance = 0
                for idy, edge in enumerate(self.edges):
                    # TODO: which is the destination
                    if edge[1] == node:
                        #neighbour_node = edge[0]
                        neighbour_index = self.nodes.index(edge[0])
                        relevance += self.d * (self.relevance[neighbour_index] / self.outdegree[neighbour_index])
                self.relevance[idx] = ((1-self.d)/len(self.nodes)) + relevance

        print(self.relevance, "\n max is: ", np.max(self.relevance), "of node: ", self.nodes[np.argmax(self.relevance)])
        


if __name__ == "__main__" :

    xmlfile = './Sheet_05/graph.xml'
    root = parser.read_xml(xmlfile)
    nodes = parser.extract_nodes(root)
    edges = parser.extract_edges(root)
    adjacency_matrix = parser.get_adjacency_matrix(nodes, edges)
    p = PageRank(root, nodes, edges, adjacency_matrix)
    #p.iterations_pr()
    p.itr_formula()
  
