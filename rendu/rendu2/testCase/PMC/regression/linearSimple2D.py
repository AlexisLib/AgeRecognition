# Linear Model : OK
# MLP (1, 1)   : OK

from utilsRegression import *
import matplotlib.pyplot as plt
import numpy as np
from numpy.ctypeslib import ndpointer


pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

#parametre
alpha = 0.1
epochs = 10000
display = int(epochs / 10)
pmcStruct = [1]
arrStruct = (c_int * len(pmcStruct))(*pmcStruct)
c_double_p = POINTER(c_double)

X = [ 1, 2 ]
Y = [ 2, 3 ]
Xnp = np.array([ [1], [2] ])
Ynp = np.array([ 2, 3])

myDll = CDLL(pathDLL)

myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint]
myDll.loadTestCase.restype = c_void_p

pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), 2, 1, 1)
myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint]
pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), 2, 1, 0)

myDll.createPMCModel.argtypes = [POINTER(ARRAY(c_int, len(pmcStruct))), c_uint, c_uint]
myDll.createPMCModel.restype = c_void_p

pArrayWeight = myDll.createPMCModel(arrStruct, len(pmcStruct), 1)

myDll.fitPMCRegression.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_int, c_double, c_int, c_int ]
myDll.fitPMCRegression.restype = c_double								
error = myDll.fitPMCRegression( pArrayWeight, pMatrixX, pMatrixY, 2, 1, alpha, epochs, display)

myDll.datasetToVector.argtypes = [c_double_p, c_uint, c_uint]
myDll.datasetToVector.restype = c_void_p

#affichage des points
X1 = np.linspace(0, 4, 60)
myDll.predictPMCRegression.argtypes = [c_void_p, c_void_p ]
myDll.predictPMCRegression.restype = ndpointer(dtype=c_double, shape=(pmcStruct[-1],))
for x1 in X1:
	predictX = np.array([x1])
	arr_tmp = (c_double * 1)(*predictX)
	datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
	value = myDll.predictPMCRegression(pArrayWeight, datasetTmp)
	print(value[0])   
	plt.scatter(x1, value[0], color='#bbdefb')

myDll.deletePMC.argtypes = [ c_void_p ]
myDll.deletePMC(pArrayWeight)
plt.scatter(X, Y, color='red')
plt.show()
plt.clf()
      

