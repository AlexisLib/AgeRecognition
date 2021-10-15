# Linear Model x3 : OK
# MLP (2, 3)      : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *
from numpy.ctypeslib import ndpointer

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

#datas des points a tester
Xnp = np.random.random((500, 2)) * 2.0 - 1.0
Ynp = np.array([[1, 0, 0] if -p[0] - p[1] - 0.5 > 0 and p[1] < 0 and p[0] - p[1] - 0.5 < 0 else #A
              [0, 1, 0] if -p[0] - p[1] - 0.5 < 0 and p[1] > 0 and p[0] - p[1] - 0.5 < 0 else #B
              [0, 0, 1] if -p[0] - p[1] - 0.5 < 0 and p[1] < 0 and p[0] - p[1] - 0.5 > 0 else #C
              [0, 0, 0] for p in Xnp])

X = matrixToArray(Xnp.tolist())
Y = matrixToArray(Ynp.tolist())

#parametre
alpha = 0.1
epochs = 10000
display = int(epochs / 10)
pmcStruct = [2, 3]
arrStruct = (c_int * len(pmcStruct))(*pmcStruct)
c_double_p = POINTER(c_double)

myDll = CDLL(pathDLL)
myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint]
myDll.loadTestCase.restype = c_void_p

pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), Xnp.shape[0], Xnp.shape[1], 1)
myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint]
pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), Ynp.shape[0], 3, 0)

myDll.createPMCModel.argtypes = [POINTER(ARRAY(c_int, len(pmcStruct))), c_uint, c_uint]
myDll.createPMCModel.restype = c_void_p

pArrayWeight = myDll.createPMCModel(arrStruct, len(pmcStruct),  Xnp.shape[1])

myDll.fitPMCClassification.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_int, c_double, c_int, c_int ]
myDll.fitPMCClassification.restype = c_double								
error = myDll.fitPMCClassification( pArrayWeight, pMatrixX, pMatrixY, Xnp.shape[0], Xnp.shape[1], alpha, epochs, display)

myDll.datasetToVector.argtypes = [c_double_p, c_uint, c_uint]
myDll.datasetToVector.restype = c_void_p

# #A = 1
# Y1 = [ 1 if y == [1, 0, 0] else -1 for y in Y.tolist()  ]
# pArrayWeight1 = linearClassification(myDll, X, np.array(Y1), alpha, epochs, display)

# #B = 1
# Y2 = [ 1 if y == [0, 1, 0] else -1 for y in Y.tolist()  ]
# pArrayWeight2 = linearClassification(myDll, X, np.array(Y2), alpha, epochs, display)

# #A = 1
# Y3 = [ 1 if y == [0, 0, 1] else -1 for y in Y.tolist()  ]
# pArrayWeight3 = linearClassification(myDll, X, np.array(Y3), alpha, epochs, display)


#droite à tracer
X1 = np.linspace(-1, 1, 65)
X2 = np.linspace(-1, 1, 65)
myDll.predictPMCClassification.argtypes = [c_void_p, c_void_p ]
myDll.predictPMCClassification.restype = ndpointer(dtype=c_double, shape=(pmcStruct[-1],))
for x1 in X1:
	for x2 in X2: 
		predictX = np.array([x1, x2])
		arr_tmp = (c_double * 2)(*predictX)
		datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
		value = myDll.predictPMCClassification(pArrayWeight, datasetTmp)
		#value = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight1)
		print(value)
		if value[0] > value[1] and value[0] > value[2]:
			plt.scatter(x1, x2, color='#bbdefb')
		elif value[1] > value[0] and value[1] > value[2]:
		    plt.scatter(x1, x2, color='#ffcdd2')
		elif value[2] > value[0] and value[2] > value[1]:
			plt.scatter(x1, x2, color='#c8e6c9')
		else:
			plt.scatter(x1, x2, color='#eeeeee')

#affichage
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][0] == 1, enumerate(Xnp)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][0] == 1, enumerate(Xnp)))))[:,1], color='blue')
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][1] == 1, enumerate(Xnp)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][1] == 1, enumerate(Xnp)))))[:,1], color='red')
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][2] == 1, enumerate(Xnp)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Ynp[c[0]][2] == 1, enumerate(Xnp)))))[:,1], color='green')
plt.show()
plt.clf()
