# Linear Model : KO
# MLP (1, 1)   : OK

import matplotlib.pyplot as plt
import numpy as np
from utilsRegression import *

# pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

#datas des points a tester
X = np.array([ [1], [2], [3] ])
Y = np.array([ 2, 3, 2.5])

#recuperer les poids
pArrayWeight = linearRegression(myDll, X,Y)

#affichage des points
X1 = np.linspace(0, 4, 60)
for x1 in X1:
   
	predictX = np.array([x1])
	value = predict(myDll, myDll.predictLinearRegression, predictX, pArrayWeight)        
	plt.scatter(x1, value, color='#bbdefb')
      

plt.scatter(X, Y, color='red')
plt.show()
plt.clf()