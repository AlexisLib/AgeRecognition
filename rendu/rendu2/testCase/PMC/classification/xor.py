# Linear Model    : KO
# MLP (2, 2, 1)   : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *
from numpy.ctypeslib import ndpointer

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

#datas des points a tester
Xnp = np.array([[1, 0], [0, 1], [0, 0], [1, 1]])
Ynp = np.array([1, 1, -1, -1])

X = matrixToArray(Xnp.tolist())
Y = Ynp.tolist()

#parametre
alpha = 0.1
epochs = 100000
display = int(epochs / 10)
pmcStruct = [2, 2, 1]
arrStruct = (c_int * len(pmcStruct))(*pmcStruct)
c_double_p = POINTER(c_double)

myDll = CDLL(pathDLL)
myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint]
myDll.loadTestCase.restype = c_void_p

pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), Xnp.shape[0], Xnp.shape[1], 1)
myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint]
pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), Ynp.shape[0], 1, 0)

myDll.createPMCModel.argtypes = [POINTER(ARRAY(c_int, len(pmcStruct))), c_uint, c_uint]
myDll.createPMCModel.restype = c_void_p

pArrayWeight = myDll.createPMCModel(arrStruct, len(pmcStruct),  Xnp.shape[1])

myDll.fitPMCClassification.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_int, c_double, c_int, c_int ]
myDll.fitPMCClassification.restype = c_double								
error = myDll.fitPMCClassification( pArrayWeight, pMatrixX, pMatrixY, Xnp.shape[0], Xnp.shape[1], alpha, epochs, display)

myDll.datasetToVector.argtypes = [c_double_p, c_uint, c_uint]
myDll.datasetToVector.restype = c_void_p

#affichage des points
X1 = np.linspace(-2, 3, 30)
X2 = np.linspace(-2, 3, 30)
myDll.predictPMCClassification.argtypes = [c_void_p, c_void_p ]
myDll.predictPMCClassification.restype = ndpointer(dtype=c_double, shape=(pmcStruct[-1],))
for x1 in X1:
    for x2 in X2: 
        predictX = np.array([x1, x2])
        arr_tmp = (c_double * 2)(*predictX)
        datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
        value = myDll.predictPMCClassification(pArrayWeight, datasetTmp)
        if value == 1:
            plt.scatter(x1, x2, color='#bbdefb')
        else:
            plt.scatter(x1, x2, color='#ffcdd2')

plt.scatter(Xnp[0:2, 0], Xnp[0:2, 1], color='blue')
plt.scatter(Xnp[2:4,0], Xnp[2:4,1], color='red')
plt.show()
plt.clf()

