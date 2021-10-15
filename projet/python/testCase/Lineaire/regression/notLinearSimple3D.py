# Linear Model       : KO
# MLP (2, 2, 1)      : OK
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from utilsRegression import *

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

# Points Data
Xnp = np.array([ [1, 0], [0, 1], [1, 1], [0, 0] ])
Ynp = np.array([ 1, 2, 3, 4 ])
Y = Ynp.tolist()

# Get Weights
pArrayWeight = linearRegression(myDll, Xnp,Ynp)

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(Xnp[:,0], Xnp[:,1], Y, color="red")
XX, YY, ZZ = [], [], []

# Predict points to test if Model is working 
for x1 in range(0, 500, 10):
	for x2 in range(0, 500, 10):
		x1 /= 100
		x2 /= 100
		XX.append(x1)
		YY.append(x2)
		predictX = np.array([x1, x2])
		zz = predict(myDll, myDll.predictLinearRegression, predictX, pArrayWeight)
		ZZ.append(zz)

ax.plot_trisurf(XX, YY, ZZ, lw=0, color="grey", alpha=0.5)
plt.show()

# delete linear Model (free)
myDll.deleteLinearModel.argtypes = [ c_void_p ]
myDll.deleteLinearModel( pArrayWeight )
