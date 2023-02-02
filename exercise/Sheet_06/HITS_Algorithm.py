import numpy as np
import random
import parser

class HITS():
	def __init__(self, root, nodes, node_names, edges, adjacency_matrix, query=None, iterations=10):
		#
		self.itr = iterations
		self.root = root
		self.chapters = nodes
		print("no of chapters", len(nodes))
		self.chapter_names = node_names
		self.links = edges
		self.adjacency_matrix  = adjacency_matrix
		#
		self.hub_weights = np.full(len(nodes), 1)
		self.authorities = np.full(len(nodes), 1)
		self.base_graph = None
		#
		self.d = 5  # max no of inward nodes to consider
		if query != None:
			self.query_string = query
			self.root_graph_init_Extended()  # another algo
			#self.root_graph_init()
		

	def root_graph_simple(self):
		temp_list=[]
		for i, ch in enumerate(self.chapters):
			temp_list.append((i,ch))
		self.base_graph = temp_list.copy()

	def root_graph_init(self):
		query_nodes = []
		for idx, chapter in enumerate(self.chapter_names):
			if self.query_string in chapter:
				query_nodes.append((idx, self.chapters[idx]))
		self.base_graph = query_nodes
	
	def root_graph_init_Extended(self):
		# add all the incoming nodes to the graph
		self.root_graph_init()
		graph_temp = self.base_graph.copy()
		for idx, chapter in enumerate(self.base_graph):
			inward_nodes=[]
			for idy, link in enumerate(self.links):
				# Incoming
				if link[1] == chapter[1]:
					source_node_index = self.chapters.index(link[0])
					inward_nodes.append((source_node_index, link[0]))
			graph_temp = list(dict.fromkeys(graph_temp+ inward_nodes))
		#
		self.base_graph = list(dict.fromkeys(graph_temp))
		print("init", len(self.base_graph))


	def root_graph_expansion(self):
		prev_length = len(self.base_graph)
		root_graph_nodes = self.base_graph.copy()
		for idx, chapter in enumerate(self.base_graph):
			# chapter is a tuple of (idx, name)
			inward_nodes = []
			for idy, link in enumerate(self.links):
				# Outward link
				if link[0] == chapter[1]:
					dest_node_index = self.chapters.index(link[1])
					root_graph_nodes.append((dest_node_index, link[1]))
				# Incoming
				elif link[1] == chapter[1]:
					source_node_index = self.chapters.index(link[0])
					inward_nodes.append((source_node_index, link[0]))
			# take care of large incoming nodes
			'''
			if len(inward_nodes)<self.d:
				root_graph_nodes = root_graph_nodes + inward_nodes
			else:
				root_graph_nodes = root_graph_nodes + random.sample(inward_nodes, self.d)
			'''
			root_graph_nodes = root_graph_nodes + inward_nodes
		# outside for loop
		self.base_graph = list(dict.fromkeys(root_graph_nodes))
		#
		if len(self.base_graph)>prev_length:
			print("root graph", len(self.base_graph))

	# for the whole graph
	def iterate_algo(self):
		i_counter=0
		while i_counter < self.itr:
			i_counter+=1
			#
			for idx, chapter in enumerate(self.chapters):
				sum_hubWeights = 0
				for idy, link in enumerate(self.links):
					#	
					dest_node = link[1]
					if dest_node == chapter:
						source_node_index = self.chapters.index(link[0])
						sum_hubWeights += self.hub_weights[source_node_index]
				self.authorities[idx] = sum_hubWeights
			#
			for idx, chapter in enumerate(self.chapters):
				sum_authorities = 0
				for idy, link in enumerate(self.links):
					#	
					source_node = link[0]
					if source_node == chapter:
						dest_node_index = self.chapters.index(link[1])
						sum_authorities += self.authorities[dest_node_index]
				self.hub_weights[idx] = sum_authorities
			#
			self.hub_weights = self.hub_weights / np.linalg.norm(self.hub_weights)
			self.authorities = self.authorities / np.linalg.norm(self.authorities)
			#print("best hub", np.argmax(self.authorities))
		self.show_values()
	
	# for incrementaly increasing graph
	def iterate_algo_exp(self):
		i_counter=0
		while i_counter < self.itr:
			i_counter+=1
			#
			for idx, chapter in enumerate(self.base_graph):
				sum_hubWeights = 0
				for idy, link in enumerate(self.links):
					#	
					dest_node = link[1]
					if dest_node == chapter[1]:
						source_node_index = self.chapters.index(link[0])
						sum_hubWeights += self.hub_weights[source_node_index]
				self.authorities[chapter[0]] = sum_hubWeights
			#
			for idx, chapter in enumerate(self.base_graph):
				sum_authorities = 0
				for idy, link in enumerate(self.links):
					#	
					source_node = link[0]
					if source_node == chapter[1]:
						dest_node_index = self.chapters.index(link[1])
						sum_authorities += self.authorities[dest_node_index]
				self.hub_weights[chapter[0]] = sum_authorities
			#
			self.hub_weights = self.hub_weights / np.linalg.norm(self.hub_weights)
			self.authorities = self.authorities / np.linalg.norm(self.authorities)
			self.root_graph_expansion()
		self.show_values()

	def print_with_nodes(self, array, keyword):
		print("\n", keyword, "\n")
		for i, x in enumerate(array):
			print(self.chapters[i], x)
			#print(self.chapters[i], self.chapter_names[i], x)
		
	#
	def show_values(self):
		#print("\n", "Authorities", "\n", self.authorities, "\n", "\n", "Hub_Weights", "\n", self.hub_weights)
		print("\n", "Authorities_sorted", "\n", np.sort(self.authorities)[::-1], "\n", "\n", "Hub_Weigths_sorted", "\n", np.sort(self.hub_weights)[::-1])
		self.print_with_nodes(self.authorities, "Authorities")
		self.print_with_nodes(self.hub_weights, "Hub_Weights")
		print("best Auth",self.chapters[np.argmax(self.authorities)] ,":", self.chapter_names[np.argmax(self.authorities)], "with value", np.max(self.authorities))


if __name__ == "__main__":
	#path = './Sheet_06/g2.xml'
	path = './graph.xml'
	xmlfile = path
	root = parser.read_xml(xmlfile)
	nodes = parser.extract_nodes(root)
	node_names = parser.extract_nodes_names(root)
	edges = parser.extract_edges(root)
	adjacency_matrix = parser.get_adjacency_matrix(nodes, edges)
	a = HITS(root, nodes, node_names, edges, adjacency_matrix, query=None, iterations=1000)
	a.iterate_algo_exp()
	#a.iterate_algo()
