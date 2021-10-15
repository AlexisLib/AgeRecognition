# Linear Model : KO
# MLP (1, 1)   : KO

import matplotlib.pyplot as plt
import numpy as np
from utilsRegression import *
from numpy.ctypeslib import ndpointer

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

#datas des points a tester
Xnp = np.array([ [1], [2], [3] ])
Ynp = np.array([ 2, 3, 2.5])

X = matrixToArray(Xnp.tolist())
Y = Ynp.tolist()

# Parameters
alpha = 0.01
epochs = 1000
display = int(epochs / 10)
pmcStruct = [1, 2,  1]
arrStruct = (c_int * len(pmcStruct))(*pmcStruct)
c_double_p = POINTER(c_double)

# Load Matrix X
myDll.loadTestCase.argtypes = [ POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint ]
myDll.loadTestCase.restype = c_void_p
pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), Xnp.shape[0], Xnp.shape[1], 1)

# Load Matrix Y
myDll.loadTestCase.argtypes = [ POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint ]
pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), Ynp.shape[0], 1, 0)

# Create & Allocate PMC Model using pmcStruct [1, 1]
myDll.createPMCModel.argtypes = [ POINTER(ARRAY(c_int, len(pmcStruct))), c_uint ]
myDll.createPMCModel.restype = c_void_p
pArrayWeight = myDll.createPMCModel(arrStruct, len(pmcStruct))

# Fit PMC with regression version
myDll.fitPMCRegression.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_double, c_int, c_int ]
myDll.fitPMCRegression.restype = c_double								
error = myDll.fitPMCRegression( pArrayWeight, pMatrixX, pMatrixY, 3, alpha, epochs, display)

# Prototyping the method Dataset to Vector ( double * => vectorXd)
myDll.datasetToVector.argtypes = [ c_double_p, c_uint, c_uint ]
myDll.datasetToVector.restype = c_void_p

# Prototyping the method predict PMC 
myDll.predictPMC.argtypes = [ c_void_p, c_void_p, c_int, c_int ]
myDll.predictPMC.restype = ndpointer(dtype=c_double, shape=(pmcStruct[-1],))

# Predict points to test if Model is working 
X1 = np.linspace(0, 4, 60)
for x1 in X1:
	predictX = np.array([x1])
	arr_tmp = (c_double * 1)(*predictX)
	datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
	value = myDll.predictPMC(pArrayWeight, datasetTmp, 1, 1)  
	plt.scatter(x1, value[0], color='#bbdefb')

plt.scatter(X, Y, color='red')
plt.show()
plt.clf()
      
# delete / free PMC Model
myDll.deletePMCModel.argtypes = [ c_void_p ]
myDll.deletePMCModel( pArrayWeight )