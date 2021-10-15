# Linear Model       : KO
# MLP (2, 2, 1)      : OK
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from utilsRegression import *

# pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

fig = plt.figure()
ax = Axes3D(fig)

#datas des points a tester
X = np.array([ [1, 0], [0, 1], [1, 1], [0, 0] ])
Y = np.array([ 1, 2, 3, 4 ])


pArrayWeight = linearRegression(myDll, X,Y)

#plan à tracer
X1 = np.linspace(0,5,25)
X2 = np.linspace(0,5,25)
# X1, X2 = np.meshgrid(X1, X2)

for x1 in X1:
	for x2 in X2:	
		predictX = np.array([x1, x2])
		value = predict(myDll, myDll.predictLinearRegression, predictX, pArrayWeight)
		ax.scatter(x1, x2, value, color="blue")


#affichage

ax.scatter(X[:,0],X[:,1],Y, color="red")
ax.set(xlabel="X1", ylabel="X2", zlabel="Y")
# ax.plot_surface(x1, x2, z, color='#bbdefb')
plt.show()
plt.clf()