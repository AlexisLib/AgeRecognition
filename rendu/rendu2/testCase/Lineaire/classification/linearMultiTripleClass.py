# Linear Model x3 : OK
# MLP (2, 3)      : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *

# pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

#Parametre
alpha = 0.05
epochs = 1000
display = 100

#datas des points a tester
X = np.random.random((500, 2)) * 2.0 - 1.0
Y = np.array([[1, 0, 0] if -p[0] - p[1] - 0.5 > 0 and p[1] < 0 and p[0] - p[1] - 0.5 < 0 else #A
              [0, 1, 0] if -p[0] - p[1] - 0.5 < 0 and p[1] > 0 and p[0] - p[1] - 0.5 < 0 else #B
              [0, 0, 1] if -p[0] - p[1] - 0.5 < 0 and p[1] < 0 and p[0] - p[1] - 0.5 > 0 else #C
              [0, 0, 0] for p in X])


#A = 1
Y1 = [ 1 if y == [1, 0, 0] else -1 for y in Y.tolist()  ]
pArrayWeight1 = linearClassification(myDll, X, np.array(Y1), alpha, epochs, display)

#B = 1
Y2 = [ 1 if y == [0, 1, 0] else -1 for y in Y.tolist()  ]
pArrayWeight2 = linearClassification(myDll, X, np.array(Y2), alpha, epochs, display)

#A = 1
Y3 = [ 1 if y == [0, 0, 1] else -1 for y in Y.tolist()  ]
pArrayWeight3 = linearClassification(myDll, X, np.array(Y3), alpha, epochs, display)


#droite à tracer
X1 = np.linspace(-1, 1, 65)
X2 = np.linspace(-1, 1, 65)
for x1 in X1:
	for x2 in X2: 
		predictX = np.array([x1, x2])
		value1 = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight1)
		value2 = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight2)
		value3 = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight3)

		if value1 > value2 and value1 > value3:
			plt.scatter(x1, x2, color='#bbdefb')
		elif value2 > value1 and value2 > value3:
		    plt.scatter(x1, x2, color='#ffcdd2')
		elif value3 > value1 and value3 > value2:
			plt.scatter(x1, x2, color='#c8e6c9')
		else:
			plt.scatter(x1, x2, color='#eeeeee')

#affichage
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]][0] == 1, enumerate(X)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]][0] == 1, enumerate(X)))))[:,1], color='blue')
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]][1] == 1, enumerate(X)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]][1] == 1, enumerate(X)))))[:,1], color='red')
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]][2] == 1, enumerate(X)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]][2] == 1, enumerate(X)))))[:,1], color='green')
plt.show()
plt.clf()
