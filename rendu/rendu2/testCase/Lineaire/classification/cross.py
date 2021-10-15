# Linear Model    : KO
# MLP (2, 4, 1)   : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *

# pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

#datas des points a tester
X = np.random.random((500, 2)) * 2.0 - 1.0
Y = np.array([1 if abs(p[0]) <= 0.3 or abs(p[1]) <= 0.3 else -1 for p in X])

# Parametres
alpha = 0.05
epochs = 1000
display = 10
pArrayWeight = linearClassification(myDll, X, Y, alpha, epochs, display)


#affichage des points
X1 = np.linspace(-1, 1, 30)
X2 = np.linspace(-1, 1, 30)
for x1 in X1:
    for x2 in X2: 
        predictX = np.array([x1, x2])
        value = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight)
        if value == 1:
            plt.scatter(x1, x2, color='#bbdefb')
        else:
            plt.scatter(x1, x2, color='#ffcdd2')

plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]] == 1, enumerate(X)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]] == 1, enumerate(X)))))[:,1], color='blue')
plt.scatter(np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]] == -1, enumerate(X)))))[:,0], np.array(list(map(lambda elt : elt[1], filter(lambda c: Y[c[0]] == -1, enumerate(X)))))[:,1], color='red')
plt.show()
plt.clf()

