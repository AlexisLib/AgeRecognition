# Linear Model : OK
# MLP (2, 1)   : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsRbf import *
from ctypes import *

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

# Points Data
Xnp = np.array([ [1, 5], [2, 3], [3, 3] ])
Ynp = np.array([ 1, -1, -1 ])
X = matrixToArray(Xnp.tolist())
Y = Ynp.tolist()

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
myDll.fitRBFClassification.argtypes = [ c_void_p, c_void_p, c_void_p, c_double ]							
myDll.fitRBFClassification( pArrayWeight, pMatrixX, pMatrixY, gamma)

# Prototyping the method Dataset to Vector ( double * => vectorXd)
myDll.datasetToVector.argtypes = [ c_double_p, c_uint, c_uint ]
myDll.datasetToVector.restype = c_void_p

# Prototyping the method predict RBF
myDll.predictRBFClassification.argtypes = [ c_void_p, c_void_p]
myDll.predictRBFClassification.restype = c_double


# Python Function to get coordinates
def get(i, l):
    return [z[i] for z in l]

X1 = np.linspace(0, 5, 30)
X2 = np.linspace(0, 5, 30)
classA = []
classB = []

# Predict points to test if Model is working 
for x1 in X1:
    for x2 in X2: 
        predictX = np.array([x1, x2])
        arr_tmp = (c_double * 2)(*predictX)
        datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
        value = myDll.predictRBFClassification(pArrayWeight, datasetTmp, 0, 1)
        if value > 0:
            classA.append(tuple([x1, x2]))
        else:
            classB.append(tuple([x1, x2]))

# Display points for each class
plt.scatter(
    get(0, classA),
    get(1, classA),
    color="#bbdefb"
)
plt.scatter(
    get(0, classB),
    get(1, classB),
    color="#ffcdd2"
)

# Display data points
plt.scatter(Xnp[0, 0], Xnp[0, 1], color='blue')
plt.scatter(Xnp[1:3,0], Xnp[1:3,1], color='red')
plt.show()
plt.clf()

# # delete linear Model (free)
# myDll.deleteLinearModel.argtypes = [ c_void_p ]
# myDll.deleteLinearModel( pArrayWeight )
