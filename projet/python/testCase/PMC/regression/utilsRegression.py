import matplotlib.pyplot as plt
import numpy as np
from ctypes import *

def readFileWeight(path):
	with open(path, "r") as f:
		lines = f.readline()
		weight = lines.split(";")
	weight = [float(x) for x in weight if x ]
	return tuple(weight)

def matrixToArray(matrix):
	ret = []
	for el in matrix:
		ret.extend(el)
	return ret

def pmcRegression(myDll, Xnp,Ynp, alpha, epochs, display, pmcStruct):
	X = matrixToArray(Xnp.tolist())
	Y = Ynp.tolist()

	myDll.loadTestCase.restype = c_void_p

	#charger X 
	myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint]
	pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), Xnp.shape[0],  Xnp.shape[1], 1)

	#charger Y
	myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint]
	pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), Ynp.shape[0], 1, 0)

	# Creer modele
	pmcStruct = [1, 1]
	arrStruct = (c_int * len(pmcStruct))(*pmcStruct)

	myDll.createPMCModel.argtypes = [POINTER(ARRAY(c_int, len(pmcStruct))), c_uint, c_uint]
	myDll.createPMCModel.restype = c_void_p
	pArrayWeight = myDll.createPMCModel(arrStruct, len(pmcStruct), Xnp.shape[1])

	# Entrainement
	myDll.fitPMCRegression.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_int, c_double, c_int, c_int ]
	myDll.fitPMCRegression.restype = c_double								
	error = myDll.fitPMCRegression( pArrayWeight, pMatrixX, pMatrixY, Xnp.shape[0], Xnp.shape[1], alpha, epochs, display)

	return pArrayWeight

def predictPMC(myDll, function, X, ArrayWeight):
	function.argtypes = [
							c_void_p,
							c_void_p,
						]
	function.restype = c_double
	predictResponse = function (
							ArrayWeight,
							X
						)

	return predictResponse