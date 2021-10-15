from ctypes import *
import numpy as np
import matplotlib.pyplot as plt
from numpy.ctypeslib import ndpointer
from encapsulateSharedMethods import *

def displayRBFRegResult3D(myDll, pArrayWeight, ax, X1, X2):
    XX, YY, ZZ = [], [], []
    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            datasetTmp = datasetToVector(myDll, predictX, 1)
            value = predictNaiveRBFRegression(myDll, pArrayWeight, datasetTmp)
            XX.append(x1)
            YY.append(x2)
            ZZ.append(value)
    ax.plot_trisurf(XX, YY, ZZ, lw=0, color='#bbdefb', alpha=0.5)


def displayRBFRegResult2D(myDll, pArrayWeight, X1, X2):
    for x1 in X1:
        predictX = np.array([x1])
        datasetTmp = datasetToVector(myDll, predictX, 1)
        value = predictNaiveRBFRegression(myDll, pArrayWeight, datasetTmp)     
        plt.scatter(x1, value, color='#bbdefb')

def displayRbfClassifResult2DTripleClass(myDll, pArrayWeight1, pArrayWeight2, pArrayWeight3, X1, X2):
    classA = []
    classB = []
    classC = []

    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            datasetTmp = datasetToVector(myDll, predictX, 1)
            # value1 = predictNaiveRBFClassification(myDll, pArrayWeight1, datasetTmp)
            # value2 = predictNaiveRBFClassification(myDll, pArrayWeight2, datasetTmp)
            # value3 = predictNaiveRBFClassification(myDll, pArrayWeight3, datasetTmp)
            value1 = predictNaiveRBFRegression(myDll, pArrayWeight1, datasetTmp)
            value2 = predictNaiveRBFRegression(myDll, pArrayWeight2, datasetTmp)
            value3 = predictNaiveRBFRegression(myDll, pArrayWeight3, datasetTmp)
            if value1 > value2 and value1 > value3:
                classA.append(tuple([x1, x2]))
            elif value2 > value1 and value2 > value3:
                classB.append(tuple([x1, x2]))
            elif value3 > value1 and value3 > value2:
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

def displayRbfClassifResult2D(myDll, pRBF, X1, X2):
    classA = []
    classB = []
    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            datasetTmp = datasetToVector(myDll, predictX, 1)
            value = predictNaiveRBFClassification(myDll, pRBF, datasetTmp)
            if value > 0:
                classA.append(tuple([x1, x2]))
            elif value < 0:
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

def createNaiveRBFModel(myDll, inputCountPerSample):
    myDll.createNaiveRBFModel.argtypes = [ c_uint ]
    myDll.createNaiveRBFModel.restype = c_void_p
    pRBF = myDll.createNaiveRBFModel( inputCountPerSample )
    return pRBF

def fitNaiveRBFRegression(myDll, pRBF, pMatrixX, pMatrixY, gamma):
    myDll.fitNaiveRBFRegression.argtypes = [ c_void_p, c_void_p, c_void_p, c_double ]							
    myDll.fitNaiveRBFRegression( pRBF, pMatrixX, pMatrixY, gamma )

def predictNaiveRBFRegression(myDll, pRBF, datasetVector):
    myDll.predictNaiveRBFRegression.argtypes = [ c_void_p, c_void_p]
    myDll.predictNaiveRBFRegression.restype = c_double
    result = myDll.predictNaiveRBFRegression( pRBF, datasetVector )
    return result

def fitNaiveRBFClassification(myDll, pRBF, pMatrixX, pMatrixY, gamma):
    myDll.fitNaiveRBFClassification.argtypes = [ c_void_p, c_void_p, c_void_p, c_double ]							
    myDll.fitNaiveRBFClassification( pRBF, pMatrixX, pMatrixY, gamma)

def predictNaiveRBFClassification(myDll, pRBF, datasetVector):
    myDll.predictNaiveRBFClassification.argtypes = [ c_void_p, c_void_p]
    myDll.predictNaiveRBFClassification.restype = c_double
    result = myDll.predictNaiveRBFClassification( pRBF, datasetVector )
    return result

def deleteNaiveRBFModel(myDll, pRBF):
    myDll.deleteNaiveRBFModel.argtypes = [ c_void_p ]
    myDll.deleteNaiveRBFModel( pRBF )

