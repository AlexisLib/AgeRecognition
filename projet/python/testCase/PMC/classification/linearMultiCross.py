# Linear Model x3 : KO
# MLP (2, ?, ?, 3): OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *
from numpy.ctypeslib import ndpointer

#pathDLL = "C:/Users/WT57/Documents/ProjetAnnuel3IBD-master/projet/MLAlgorithms/ML_Library/Release/ML_Library.dll"
pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

# Points Data
Xnp = np.random.random((1000, 2)) * 2.0 - 1.0
Ynp = np.array([[1, 0, 0] if abs(p[0] % 0.5) <= 0.25 and abs(p[1] % 0.5) > 0.25 else 
              [0, 1, 0] if abs(p[0] % 0.5) > 0.25 and abs(p[1] % 0.5) <= 0.25 else 
              [0, 0, 1] for p in Xnp])
X = matrixToArray(Xnp.tolist())
Y = matrixToArray(Ynp.tolist())

# Parameters
alpha = 0.001
epochs = 10000
display = int(epochs / 10)
pmcStruct = [2, 24, 24, 3]
arrStruct = (c_int * len(pmcStruct))(*pmcStruct)
c_double_p = POINTER(c_double)

# Load Matrix X
myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint]
myDll.loadTestCase.restype = c_void_p
pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), Xnp.shape[0], Xnp.shape[1], 1)

# Load Matrix Y
myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint]
pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), Ynp.shape[0], Ynp.shape[1], 0)

# Create & Allocate PMC Model using pmcStruct [2, 3]
myDll.createPMCModel.argtypes = [POINTER(ARRAY(c_int, len(pmcStruct))), c_uint]
myDll.createPMCModel.restype = c_void_p
pArrayWeight = myDll.createPMCModel(arrStruct, len(pmcStruct))

# Fit PMC with classification version
myDll.fitPMCClassification.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_double, c_int, c_int ]
myDll.fitPMCClassification.restype = c_double								
error = myDll.fitPMCClassification( pArrayWeight, pMatrixX, pMatrixY, Xnp.shape[0], alpha, epochs, display)

# Prototyping the method Dataset to Vector ( double * => vectorXd)
myDll.datasetToVector.argtypes = [c_double_p, c_uint, c_uint]
myDll.datasetToVector.restype = c_void_p

# Prototyping the method predict PMC 
myDll.predictPMC.argtypes = [c_void_p, c_void_p, c_int, c_int ]
myDll.predictPMC.restype = ndpointer(dtype=c_double, shape=(pmcStruct[-1],))

# Python Function to get coordinates
def get(i, l):
    return [z[i] for z in l]

X1 = np.linspace(-1, 1, 35)
X2 = np.linspace(-1, 1, 35)
classA = []
classB = []
classC = []

for x1 in X1:
	for x2 in X2: 
		predictX = np.array([x1, x2])
		arr_tmp = (c_double * 2)(*predictX)
		datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
		value = myDll.predictPMC(pArrayWeight, datasetTmp, 0, 1)
		if value[0] > value[1] and value[0] > value[2]:
			classA.append(tuple([x1, x2]))
		elif value[1] > value[0] and value[1] > value[2]:
		    classB.append(tuple([x1, x2]))
		elif value[2] > value[0] and value[2] > value[1]:
			classC.append(tuple([x1, x2]))

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
plt.scatter(
	get(0, classC),
	get(1, classC),
	color="#c8e6c9"
)
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][0] == 1, enumerate(Xnp)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][0] == 1, enumerate(Xnp)))))[:,1], color='blue')
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][1] == 1, enumerate(Xnp)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][1] == 1, enumerate(Xnp)))))[:,1], color='red')
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][2] == 1, enumerate(Xnp)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][2] == 1, enumerate(Xnp)))))[:,1], color='grey')
plt.show()
plt.clf()

# delete / free PMC Model
myDll.deletePMCModel.argtypes = [ c_void_p ]
myDll.deletePMCModel( pArrayWeight )

