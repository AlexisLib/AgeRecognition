# Linear Model : OK
# MLP (1, 1)   : OK

from utilsRegression import *
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


#datas des points a tester
#datas des points a tester
Xa = np.array([ [1], [2] ])
Ya = np.array([ 2, 3])

X = matrixToArray(Xa.tolist())
Y = Ya.tolist()
# X = [1, 2, 4, 6]
# Y = [2, 3]
#recuperer les poids
pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)
struct = [1, 1]
arr_struct = (c_int * len(struct))(*struct)

myDll.loadTestCase.argtypes = [
	POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint]
myDll.loadTestCase.restype = c_void_p

pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), 2, 1, 1)
myDll.loadTestCase.argtypes = [
	POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint]
pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), 2, 1, 0)

print("debut create")
myDll.createPMCModel.argtypes = [POINTER(ARRAY(c_int, 2)), c_uint, c_uint]
myDll.createPMCModel.restype = c_void_p

W = myDll.createPMCModel(arr_struct, len(struct), 2)
print("fin create")

myDll.fitPMCRegression.argtypes = [
	c_void_p, c_void_p, c_void_p, c_int, c_int, c_double, c_int, c_int]
myDll.fitPMCRegression.restype = c_double
error = myDll.fitPMCRegression(W, pMatrixX, pMatrixY, 2, 1, 0.1, 1000, 10)

#droite à tracer
c_double_p = POINTER(c_double)
myDll.datasetToVector.argtypes = [c_double_p, c_uint, c_uint]
myDll.datasetToVector.restype = c_void_p

myDll.predictPMCRegression.argtypes = [c_void_p, c_void_p]
myDll.predictPMCRegression.restype = c_double

#plan à tracer
x1 = np.linspace(0, 5, 30)
x2 = np.linspace(0, 5, 30)
#x1, x2 = np.meshgrid(x1, x2)

#affichage
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(Xa[:, 0], Xa[:, 1], Ya)
#ax.plot_surface(x1, x2, z, color='#bbdefb')

for x in x1:
        for y in x2:
                tmp = []
                tmp.append(x)
                tmp.append(y)
                arr_K = (c_double * len(tmp))(*tmp)
                datasetX = myDll.datasetToVector(arr_K, 2, 1)
                res = myDll.predictPMCRegression(W, datasetX)

                a = np.array([x1])
                b = np.array([x2])
                c = np.array([res])
                ax.scatter(a, b, c, color='green')

#affichage

plt.show()
plt.clf()
