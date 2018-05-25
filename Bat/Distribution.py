import numpy as np
import time

class Distribution:
	seed = int(time.time())
	random_generator = np.random.RandomState(seed)

	@staticmethod
	def setSeed(s):
		Distribution.seed = s
		Distribution.random_generator.seed(s)

	@staticmethod
	def getSeed():
		return Distribution.seed

	@staticmethod
	def uniform():
		return Distribution.random_generator.uniform()

	@staticmethod
	def uniform(n):
		if n <= 0:
			raise Exception("Must be positive")
		else:
			return Distribution.random_generator.uniform(0, n)

	@staticmethod
	def uniform(a, b):
		if (b <= a):
			raise Exception("Invalid range")
		else:
			return Distribution.random_generator.uniform(a, b)