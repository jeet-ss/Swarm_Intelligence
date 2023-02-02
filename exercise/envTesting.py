import numpy as np
from itertools import cycle
#import gym

class People():
	def __init__(self, x=3, y="abdc"):
		self.func2()
	

	def func1(self):
		switch={
			'a':self.func2(),
			'b':self.func3()
		}

	def func2(self):
		c=0
		d=0
		x=[1,2,3]
		while True:
			for i in range(len(x)):
				#print(i, len(x))
				k = (i + 1) % len(x)
				print("dd",  x[k], k)
			c += 1
			if c>2:
				break

	def func3(self, c):
		print("loser")


if __name__ == "__main__":
	p = People()
