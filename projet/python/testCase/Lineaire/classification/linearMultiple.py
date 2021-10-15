# Linear Model : OK
# MLP (2, 1)   : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

# Points Data
# Points Data
Xnp = np.concatenate([np.random.random((50,2)) * 0.9 + np.array([1, 1]), np.random.random((50,2)) * 0.9 + np.array([2, 2])])
Ynp = np.concatenate([np.ones((50, 1)), np.ones((50, 1)) * -1.0])
Ynp = Ynp.flatten()

X = matrixToArray(Xnp.tolist())
Y = Ynp.tolist()

# Parameters
alpha = 0.01
epochs = 1000
display = int(epochs / 10)

pArrayWeight = linearClassification(myDll, Xnp, Ynp, alpha, epochs, display)

# Python Function to get coordinates
def get(i, l):
    return [z[i] for z in l]

X1 = np.linspace(1, 3, 30)
X2 = np.linspace(1, 3, 30)
classA = []
classB = []

# Predict points to test if Model is working 
for x1 in X1:
    for x2 in X2: 
        predictX = np.array([x1, x2])
        arr_tmp = (c_double * 2)(*predictX)
        datasetTmp = myDll.datasetToVector(arr_tmp, len(predictX), 1)
        value = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight)
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
plt.scatter(Xnp[0:50, 0], Xnp[0:50, 1], color='blue')
plt.scatter(Xnp[50:100,0], Xnp[50:100,1], color='red')
plt.show()
plt.clf()

# delete linear Model (free)
myDll.deleteLinearModel.argtypes = [ c_void_p ]
myDll.deleteLinearModel( pArrayWeight )