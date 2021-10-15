# Linear Model    : KO
# MLP (2, 2, 1)   : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

# Points Data
Xnp = np.array([[1, 0], [0, 1], [0, 0], [1, 1]])
Ynp = np.array([1, 1, -1, -1])
X = matrixToArray(Xnp.tolist())
Y = Ynp.tolist()

# Parameters
alpha = 0.001
epochs = 100000
display = int(epochs / 10)

pArrayWeight = linearClassification(myDll, Xnp, Ynp, alpha, epochs, display)

# Python Function to get coordinates
def get(i, l):
    return [z[i] for z in l]

#affichage des points
X1 = np.linspace(-0.5, 1.5, 30)
X2 = np.linspace(-0.5, 1.5, 30)
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

plt.scatter(Xnp[0:2, 0], Xnp[0:2, 1], color='blue')
plt.scatter(Xnp[2:4,0], Xnp[2:4,1], color='red')
plt.show()
plt.clf()

# delete linear Model (free)
myDll.deleteLinearModel.argtypes = [ c_void_p ]
myDll.deleteLinearModel( pArrayWeight )
