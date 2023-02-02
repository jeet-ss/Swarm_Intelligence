import numpy as np
from torch import le, ne


# Particle Swarm Optimization
class PSO():
	def __init__(self, a, b_loc, b_glob, N, dim,
				 boundary_max, obj_function, boundary_condt,
				 toplogy,
				 ):
		# iteration counter
		self.c=0
		# constants
		self.a = a 
		self.b_loc = b_loc
		self.b_glob = b_glob
		self.dim = dim  
		self.N = N  # no of particles
		self.boundary_max = boundary_max
		self.topology = toplogy
		self.neighbourhood = np.array([])
		# load the obj function
		self.obj_function = self.load_objectiveFunction(obj_function)
		# boundary condition
		self.boundary_condt = self.load_boundaryFunction(boundary_condt)
		# Initialize the particles position
		self.x_i = np.random.uniform(-self.boundary_max, self.boundary_max, (N, self.dim))
		# Initialize the velocity , each dimension
		self.v_i = np.zeros((N, self.dim))
		# set the local best position
		self.p_i = self.x_i.copy()
		# init P_glob
		#self.p_glob = self.init_pGlob(self.p_i)  # best location
		self.p_glob = self.load_topologyFunction(self.topology)
		#print("glob", self.p_glob.shape, self.neighbourhood.shape)

	# init pglob
	def pglob_fullyconnected(self):
		out = []
		for idx in range(self.N):
			out.append(self.capital_F(self.x_i[idx], idx))
		return self.x_i[np.argmin(out)]  # a (1,d) dim vector
	
	def compute_p_glob_matrix(self):
		p_glob = np.array(np.arange(self.dim))
		for ele in self.neighbourhood:
			locs = np.array(np.arange(self.dim))
			for x in ele:
				locs = np.vstack((locs, self.p_i[x]))
			# remove the 1st list
			locs = locs[1:,:]
			max = 0
			best_pos = np.array([])
			for y in locs:
				val = self.obj_function(y)  # 1 given as a placeholder
				if val>max:
					max = val
					best_pos = y
			p_glob = np.vstack((p_glob, best_pos))
		
		p_glob=p_glob[1:,:]
		return p_glob

	
	def neighbourhood_loader(self, pattern_):
		# pattern = np.array([-1, 0 ,1])
		pattern = pattern_
		neighbours = np.stack([np.arange(self.N)]*len(pattern)).T
		neighbours = (neighbours + pattern) % self.N
		return neighbours

	# load the topology
	def load_topologyFunction(self, text="Fully"):
		if text == "Ring":
			pattern = np.array([-1, 0 ,1])
			self.neighbourhood = self.neighbourhood_loader(pattern)
			p_glob = self.compute_p_glob_matrix()
			return p_glob
		elif text == "Mesh":
			size = int(self.N**(1/2))
			pattern = np.array([-1, 0, 1, -size, size])
			self.neighbourhood = self.neighbourhood_loader(pattern)
			p_glob = self.compute_p_glob_matrix()
			return p_glob
		else:
			self.neighbourhood = None
			p_glob = self.pglob_fullyconnected()
			return p_glob


	# load the obj
	def load_objectiveFunction(self, text="Sphere"):
		switch = {
			"Sphere": self.sphere,
			"Rosenbrock" : self.rosenbrock,
			"Rastrigin" : self.rastrigin,
			"Schwefel" : self.schwefel
		}
		return switch.get(text, self.sphere)

	# set the boundary condition
	def load_boundaryFunction(self, text="Infinity"):
		switch={
			"Infinity": self.infinity_boundary,
			"Absorb": self.absorb_boundary,
			"Mirror": self.mirror_boundary,
		}
		return switch.get(text, np.inf)

	# 
	def infinity_boundary(self, x, idx):
		return np.inf

	# Absorb Boundary
	def absorb_boundary(self, x, idx):
		# set velocity to zero
		v_temp = [0 for i in self.v_i[idx]]
		self.v_i[idx] = v_temp
		# TODO: which value to return for the particle
		# return np.inf

	# 
	def mirror_boundary(self, x, idx):
		# set position to best global
		self.x_i[idx] = self.p_i[idx]
		x = self.x_i[idx]
		# return the value of p_loc as the value of the point
		return self.obj_function(x)

	# check boundary
	def check_boundary(self, x):
		flag = False
		# check bounday crossing for individual particle
		for i in range(x.shape[0]):
			if x[i] > self.boundary_max or x[i] < -self.boundary_max:
				flag = True
				#print("boundary", x[i])
		return flag

	# General objective Funciton
	def capital_F(self, x, idx):  # x : (d,)
		flag = self.check_boundary(x)
		# if outside boudary
		if flag == True:
			return self.boundary_condt(x, idx)
		# if inside boundary
		elif flag == False:
			return self.obj_function(x)

	# Sphere objective function
	def sphere(self, x):  # inp: (d,)
		return np.sum(x * x)  # a scalar value

	# Rosenbrock objective Function		
	def rosenbrock(self, x):  # inp: (d,)	
		out_r = []
		for i in range(self.dim-1):
			out_r.append(((100*((x[i+1]- (x[i]**2))**2) +\
				((1 - x[i])**2))))

		return np.sum(out_r)  # scalar

	# Rastrigin objective function
	def rastrigin(self, x):  # inp: (d,)
		out_r = []
		for i in range(self.dim):
			out_r.append((x[i]**2) - 10*np.cos(2*np.pi*x[i]))
			
		return ( 10*self.dim + np.sum(out_r))  # a scalar value

	# Schwefel objective function
	def schwefel(self, x):  # inp: (d,)
		out_r = []
		for i in range(self.dim):
			out_r.append((-x[i]) * np.sin(np.sqrt(np.abs(x[i]))))
			
		return np.sum(out_r) # a scalar value

	def best_position(self):
		max=0
		best_pos = np.array([])
		for ele in self.p_glob:
			best_pos = np.append(best_pos, self.obj_function(ele))
		return self.p_glob[np.argmin(best_pos)]


	# PSO algo- ring
	def algo_topo(self):
		
		# simulation of swarm behavior
		while True:
			self.c += 1
			# random intialization
			self.r_loc = np.random.uniform(0.0, 1.0, (1, self.dim))
			self.r_glob = np.random.uniform(0.0, 1.0, (1, self.dim))
			# simulation of individual particles
			for idx in range(self.N):
				# movement equations
				self.v_i[idx] = self.a * self.v_i[idx] + \
								self.b_glob * (self.r_glob * (self.p_glob[idx] - self.x_i[idx])) + \
								self.b_loc * (self.r_loc * (self.p_i[idx] - self.x_i[idx]))
				# since c=d=1
				self.x_i[idx] = self.x_i[idx] + self.v_i[idx]

			# update local and global attractors
			for index in range(self.N):

				if self.capital_F(self.x_i[index], index) <= \
					self.capital_F(self.p_i[index], index):
					# set new value
					self.p_i[index] = self.x_i[index]
				
				# TODO: How to update the p_global ??
				
				'''
				if self.capital_F(self.x_i[index], index) <= \
					self.capital_F(self.p_glob[index], index):
					# store global best
					self.p_glob[index] = self.x_i[index]
				'''
			# recompute pglob after each iteration
			self.p_glob = self.compute_p_glob_matrix()
			
			# run limit
			if self.c > 10000:
				best=self.best_position()
				print("best point", self.p_glob.shape, best)
				break
		
	def algo(self):
		# simulation of swarm behavior
		while True:
			self.c += 1
			# random intialization
			self.r_loc = np.random.uniform(0.0, 1.0, (1, self.dim))
			self.r_glob = np.random.uniform(0.0, 1.0, (1, self.dim))
			# simulation of individual particles
			for idx in range(self.N):
				# movement equations
				self.v_i[idx] = self.a * self.v_i[idx] + \
								self.b_glob * (self.r_glob * (self.p_glob - self.x_i[idx])) + \
								self.b_loc * (self.r_loc * (self.p_i[idx] - self.x_i[idx]))
				# since c=d=1
				self.x_i[idx] = self.x_i[idx] + self.v_i[idx]

			# update local and global attractors
			for index in range(self.N):

				if self.capital_F(self.x_i[index], index) < \
					self.capital_F(self.p_i[index], index):
					# set new value
					self.p_i[index] = self.x_i[index]
				
				if self.capital_F(self.x_i[index], index) < \
					self.capital_F(self.p_glob, index):
					# store global best
					self.p_glob = self.x_i[index]

			# termination criteria
			#if F (~xmin ) = min(F (~x) | ~x ∈ Rd ) 
			
			# run limit
			if self.c > 100000:
				print("best point", self.p_glob )
				break

if __name__ == "__main__":
	particle=PSO(a = 0.72984, b_loc = 1.496172, b_glob = 1.496172,
	 			N=14, dim=16, boundary_max=100, obj_function="Schwefel",
				boundary_condt="Infinity", toplogy="Mesh")
	particle.algo_topo()	
	#print(particle.c)