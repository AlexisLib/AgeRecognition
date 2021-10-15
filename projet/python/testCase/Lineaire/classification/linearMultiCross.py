# Linear Model x3 : KO
# MLP (2, ?, ?, 3): OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *


pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)


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


#A = 1
Y1 = [ 1 if y == [1, 0, 0] else -1 for y in Ynp.tolist()  ]
pArrayWeight1 = linearClassification(myDll, Xnp, np.array(Y1), alpha, epochs, display)

#B = 1
Y2 = [ 1 if y == [0, 1, 0] else -1 for y in Ynp.tolist()  ]
pArrayWeight2 = linearClassification(myDll, Xnp, np.array(Y2), alpha, epochs, display)

#A = 1
Y3 = [ 1 if y == [0, 0, 1] else -1 for y in Ynp.tolist()  ]
pArrayWeight3 = linearClassification(myDll, Xnp, np.array(Y3), alpha, epochs, display)

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
		value1 = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight1)
		value2 = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight2)
		value3 = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight3)

		if value1 > value2 and value1 > value3:
			classA.append(tuple([x1, x2]))
		elif value2 > value1 and value2 > value3:
		    classB.append(tuple([x1, x2]))
		elif value3 > value1 and value3 > value2:
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

# delete linear Model (free)
myDll.deleteLinearModel.argtypes = [ c_void_p ]
myDll.deleteLinearModel( pArrayWeight1 )
myDll.deleteLinearModel( pArrayWeight2 )
myDll.deleteLinearModel( pArrayWeight3 )