from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from random import uniform


fig = plt.figure()
ax = Axes3D(fig)
ax.set(xlabel="X1", ylabel="X2", zlabel="Y")


trainX = np.array([[x1,x2] for x1 in range(30) for x2 in range(30)])
trainY = np.array([4.5*x1 - 2.3*x2 + uniform(-2,2) for x1 in range(30) for x2 in range(30)])

ax.scatter(trainX[:,0], trainX[:,1], trainY)
plt.show()