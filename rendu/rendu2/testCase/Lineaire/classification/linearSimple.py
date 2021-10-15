# Linear Model : OK
# MLP (2, 1)   : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsClassification import *
from ctypes import *

# pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

#datas des points a tester
X = np.array([ [1, 1], [2, 3], [3, 3] ])
Y = np.array([ 1, -1, -1 ])

#parametre
alpha = 0.05
epochs = 1000
display = 100		#a debuger

pArrayWeight = linearClassification(myDll, X, Y, alpha, epochs, display)

#affichage des points
X1 = np.linspace(0, 4, 30)
X2 = np.linspace(0, 4, 30)
for x1 in X1:
    for x2 in X2: 
        predictX = np.array([x1, x2])
        value = predict(myDll, myDll.predictLinearClassification, predictX, pArrayWeight)
        if value == 1:
            plt.scatter(x1, x2, color='#bbdefb')
        else:
            plt.scatter(x1, x2, color='#ffcdd2')

plt.scatter(X[0, 0], X[0, 1], color='blue')
plt.scatter(X[1:3,0], X[1:3,1], color='red')
plt.show()
plt.clf()