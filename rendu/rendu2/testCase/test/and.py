from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from utilsRegression import *

#datas des points a tester
X = np.array([[1, 0], [0, 1], [0, 0], [1, 1]])
Y = np.array([-1, -1,-1 , 1])

w1, w2, w3 = linearRegression(X,Y, "and.csv")

#plan à tracer
x1 = np.linspace(0,2,40)
x2 = np.linspace(0,2,40)
x1, x2 = np.meshgrid(x1, x2)
z = 1 * w1 + x1 * w2 + x2 * w3

#affichage
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(X[:,0],X[:,1],Y)
ax.plot_surface(x1, x2, z, color='#bbdefb')
plt.show()
plt.clf()
