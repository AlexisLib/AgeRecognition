from ctypes import *
import matplotlib.pyplot as plt
import numpy as np
import cvxopt.base
from encapsulateSharedMethods import *

def displaySVMKernelClassifResult2DTripleClass(myDll, W0A, W0B, W0C, alphaVectorA, alphaVectorB, alphaVectorC, pMatrixX, pMatrixYA, pMatrixYB, pMatrixYC, X1, X2):
    classA = []
    classB = []
    classC = []

    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            datasetTmp = datasetToVector(myDll, predictX, 0)
            value1 = predictSvmKernelTrickClassification(myDll, pMatrixX, pMatrixYA, datasetTmp, alphaVectorA, W0A)
            value2 = predictSvmKernelTrickClassification(myDll, pMatrixX, pMatrixYB, datasetTmp, alphaVectorB, W0B)
            value3 = predictSvmKernelTrickClassification(myDll, pMatrixX, pMatrixYC, datasetTmp, alphaVectorC, W0C)

            if value1 >= value2 and value1 >= value3:
                classA.append(tuple([x1, x2]))
            elif value2 >= value1 and value2 >= value3:
                classB.append(tuple([x1, x2]))
            elif value3 >= value1 and value3 >= value2:
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

def displaySVMKerneltrickClassifResult2D(myDll, W0, pMatrixX, pMatrixY,alphaVector, X1, X2):
    classA = []
    classB = []
    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            datasetTmp = datasetToVector(myDll, predictX, 0)
            value = predictSvmKernelTrickClassification(myDll, pMatrixX, pMatrixY, datasetTmp, alphaVector, W0)
            if value > 0:
                classA.append(tuple([x1, x2]))
            else:
                classB.append(tuple([x1, x2]))
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

def displaySVMRegResult2D(myDll, WVector, X1):
    for x1 in X1:
        predictX = np.array([x1])
        pMatrixX = loadTestCase(myDll, predictX, 1, len(predictX), 1)
        value = predictSvmRegression(myDll, WVector, pMatrixX)  
        plt.scatter(x1, value, color='#bbdefb')

def displaySVMClassifResult2DTripleClass(myDll, WVector1, WVector2, WVector3, X1, X2):
    classA = []
    classB = []
    classC = []

    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            pMatrixX = loadTestCase(myDll, predictX, 1, len(predictX), 1)
            value1 = predictSvmClassification(myDll, WVector1, pMatrixX)
            value2 = predictSvmClassification(myDll, WVector2, pMatrixX)
            value3 = predictSvmClassification(myDll, WVector3, pMatrixX)

            if value1 >= value2 and value1 >= value3:
                classA.append(tuple([x1, x2]))
            elif value2 >= value1 and value2 >= value3:
                classB.append(tuple([x1, x2]))
            elif value3 >= value1 and value3 >= value2:
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

def displaySVMClassifResult2D(myDll, WVector, X1, X2):
    classA = []
    classB = []
    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            pMatrixX = loadTestCase(myDll, predictX, 1, len(predictX), 1)
            value = predictSvmClassification(myDll, WVector, pMatrixX)
            if value > 0:
                classA.append(tuple([x1, x2]))
            else:
                classB.append(tuple([x1, x2]))
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

def predictSvmClassification(myDll, WVector, pMatrixX):
    myDll.predictSvmClassification.argtypes = [ c_void_p , c_void_p ]
    myDll.predictSvmClassification.restype = c_double   
    result = myDll.predictSvmClassification(WVector, pMatrixX)
    return result

def predictSvmRegression(myDll, WVector, pMatrixX):
    myDll.predictSvmRegression.argtypes = [ c_void_p , c_void_p ]
    myDll.predictSvmRegression.restype = c_double   
    result = myDll.predictSvmRegression(WVector, pMatrixX)
    return result

def predictSvmKernelTrickClassification(myDll, pMatrixX, pMatrixY, datasetTmp, alphaVector, W0):
    myDll.predictSvmKernelTrickClassification.argtypes = [ c_void_p , c_void_p, c_void_p, c_void_p, c_double]
    myDll.predictSvmKernelTrickClassification.restype = c_double
    value = myDll.predictSvmKernelTrickClassification(pMatrixX, pMatrixY, datasetTmp, alphaVector, W0)
    return value

def fitSvmKernelTrick(myDll, pMatrixX, pMatrixY, alphaVector):
    myDll.fitSvmKernelTrick.argtypes = [c_void_p, c_void_p, c_void_p]
    myDll.fitSvmKernelTrick.restype = c_double
    W0 = myDll.fitSvmKernelTrick(pMatrixX, pMatrixY, alphaVector)
    return W0

def fitSvm(myDll, pMatrixX, pMatrixY, alphaVector):
    myDll.fitSvm.argtypes = [c_void_p, c_void_p, c_void_p]
    myDll.fitSvm.restype = c_void_p
    WVector = myDll.fitSvm(pMatrixX, pMatrixY, alphaVector)
    return WVector

def getAlpha(bigMatrix, Y):
# Define problem data
    q = np.ones(bigMatrix.shape[0])
    q = cvxopt.matrix(-q)

    n = bigMatrix.shape[0]

    bigMatrix = cvxopt.matrix(bigMatrix)
    A = cvxopt.matrix(Y.T, (1, n))
    b = cvxopt.matrix(0.0)
    G = cvxopt.matrix(np.diag(np.ones(n) * -1.0))
    h = cvxopt.matrix(np.zeros(n))
    cvxopt.solvers.options['show_progress'] = False
    solution = cvxopt.solvers.qp(bigMatrix, q, G, h, A, b)
    alphas = np.ravel(solution['x'])
    return alphas

def getBigMatrix(X, Y):
    bigMatrix = np.empty(shape=(X.shape[0], X.shape[0]))
    for i in range(0, X.shape[0]):
        for j in range(0, X.shape[0]):
            bigMatrix[i][j] = np.dot(X[i],np.transpose(X[j])) * (Y[i] * Y[j])
    return bigMatrix

def kernelTrick(n,m):
    return (np.exp(-np.dot(m, m)) * np.exp(-np.dot(n, n)) * np.exp(2 * np.dot(n, m)))



def getBigMatrixKernelTrick(X, Y):
    bigMatrix = np.empty(shape=(X.shape[0], X.shape[0]))
    for i in range(0, X.shape[0]):
        for j in range(0, X.shape[0]):
            bigMatrix[i][j] = kernelTrick(X[i], X[j]) * (Y[i] * Y[j])
    return bigMatrix
