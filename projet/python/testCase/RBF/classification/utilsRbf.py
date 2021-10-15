import matplotlib.pyplot as plt
import numpy as np
from ctypes import *

def matrixToArray(matrix):
	ret = []
	for el in matrix:
		ret.extend(el)
	return ret