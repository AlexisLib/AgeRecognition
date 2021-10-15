# Linear Model : OK
# MLP (1, 1)   : OK

from ctypes import *
import matplotlib.pyplot as plt
import numpy as np

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "C:/Users/WT57/Documents/ProjetAnnuel3IBD-master/projet/MLAlgorithms/ML_Library/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

# Points Data
X = [ 1, 2 ]
Y = [ 2, 3 ]
Xnp = np.array([ [1], [2] ])
Ynp = np.array([ 2, 3])

# Parameters
gamma = 0.5
c_double_p = POINTER(c_double)

# Load Matrix X
myDll.loadTestCase.argtypes = [ POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint ]
myDll.loadTestCase.restype = c_void_p
pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), Xnp.shape[0], Xnp.shape[1], 1)

# Load Matrix Y
myDll.loadTestCase.argtypes = [ POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint ]
pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), Ynp.shape[0], 1, 0)

# Create & Allocate RBF Model
myDll.createRBFModel.argtypes = [ c_uint ]
myDll.createRBFModel.restype = c_void_p
pArrayWeight = myDll.createRBFModel(Xnp.shape[1])

# Fit RBF with regression version
myDll.fitRBFRegression.argtypes = [ c_void_p, c_void_p, c_void_p, c_double ]							
error = myDll.fitRBFRegression( pArrayWeight, pMatrixX, pMatrixY, gamma)

# Prototyping the method Dataset to Vector ( double * => vectorXd)
myDll.datasetToVector.argtypes = [ c_double_p, c_uint, c_uint ]
myDll.datasetToVector.restype = c_void_p

# Prototyping the method predict RBF
myDll.predictRBFRegression.argtypes = [ c_void_p, c_void_p]
myDll.predictRBFRegression.restype = c_double

# Predict points to test if Model is working 
X1 = np.linspace(0, 4, 60)
for x1 in X1:
	predictX = np.array([x1])
	arr_tmp = (c_double * 1)(*predictX)
	datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
	value = myDll.predictRBFRegression(pArrayWeight, datasetTmp)  
	plt.scatter(x1, value, color='#bbdefb')

plt.scatter(X, Y, color='red')
plt.show()
plt.clf()

# # delete / free PMC Model
# myDll.deletePMCModel.argtypes = [ c_void_p ]
# myDll.deletePMCModel( pArrayWeight )
      


