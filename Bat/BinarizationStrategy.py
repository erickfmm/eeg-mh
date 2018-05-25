import numpy as np
import Bat.Distribution as Distribution

def sShape1(x):
	return (1 / (1 + (np.e ** (-2 * x))))

def standard(x):
	return 1 if x <= Distribution.uniform() <= x else 0

def toBinary(x):
	return standard(sShape1(x))