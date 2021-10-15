# Linear Model    : OK
# MLP (2, 1)      : OK

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from utilsRegression import *
from numpy.ctypeslib import ndpointer

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "C:/Users/WT57/Documents/ProjetAnnuel3IBD-master/projet/MLAlgorithms/ML_Library/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

# Points Data
Xnp = np.array([ [1, 1], [2, 2], [3, 1] ])
Ynp = np.array([ 2, 3, 2.5 ])
X = matrixToArray(Xnp.tolist())
Y = Ynp.tolist()

# Parameters
alpha = 0.01
epochs = 10000
display = int(epochs / 10)
pmcStruct = [2,  1]
arrStruct = (c_int * len(pmcStruct))(*pmcStruct)
c_double_p = POINTER(c_double)

# Load Matrix X
myDll.loadTestCase.argtypes = [ POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint ]
myDll.loadTestCase.restype = c_void_p
pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), Xnp.shape[0], Xnp.shape[1], 1)

# Load Matrix Y
myDll.loadTestCase.argtypes = [ POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint ]
pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), Ynp.shape[0], 1, 0)

# Create & Allocate PMC Model using pmcStruct [2, 1]
myDll.createPMCModel.argtypes = [ POINTER(ARRAY(c_int, len(pmcStruct))), c_uint ]
myDll.createPMCModel.restype = c_void_p
pArrayWeight = myDll.createPMCModel(arrStruct, len(pmcStruct))


# Fit PMC with regression version
myDll.fitPMCRegression.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_double, c_int, c_int ]
myDll.fitPMCRegression.restype = c_double								
error = myDll.fitPMCRegression( pArrayWeight, pMatrixX, pMatrixY, Xnp.shape[0],  alpha, epochs, display)
							

# Prototyping the method Dataset to Vector ( double * => vectorXd)
myDll.datasetToVector.argtypes = [ c_double_p, c_uint, c_uint ]
myDll.datasetToVector.restype = c_void_p

# Prototyping the method predict PMC 
myDll.predictPMC.argtypes = [ c_void_p, c_void_p, c_int, c_int ]
myDll.predictPMC.restype = ndpointer(dtype=c_double, shape=(pmcStruct[-1],))

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(Xnp[:,0], Xnp[:,1], Y, color="red")
XX, YY, ZZ = [], [], []

for x1 in range(0, 500, 10):
	for x2 in range(0, 500, 10):
		x1 /= 100
		x2 /= 100
		XX.append(x1)
		YY.append(x2)
		predictX = np.array([x1, x2])
		arr_tmp = (c_double * 2)(*predictX)
		datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
		zz = myDll.predictPMC(pArrayWeight, datasetTmp, 1, 1)
		ZZ.append(zz[0])

ax.plot_trisurf(XX, YY, ZZ, lw=0, color="grey", alpha=0.5)
plt.show()

# delete / free PMC Model
myDll.deletePMCModel.argtypes = [ c_void_p ]
myDll.deletePMCModel( pArrayWeight )