import numpy as np
import tsplib95 as tp
import parser_tsp

class Ant_algo():
    def __init__(self, alp, betn ):
        # 
        pass
        
    def algo(self):
        pass


if __name__ == "__main__":
    file_path = './Sheet_07/ulysses16.tsp'
    adjacency_matrix = parser_tsp.mk_adj(file_path)
    print(adjacency_matrix)
    ant = Ant_algo()