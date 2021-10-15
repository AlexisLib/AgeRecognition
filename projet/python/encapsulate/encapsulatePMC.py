from ctypes import *
import numpy as np
import matplotlib.pyplot as plt
from numpy.ctypeslib import ndpointer
from encapsulateSharedMethods import *

def	predictPMCRegressionAverageWithMinMax(myDll, tabSelectedImages, pArrayWeight, imageW, imageH, component, display, is255, ageMin, ageMax):
    average = 0

    for image in tabSelectedImages:
        imageName = image[image.rfind("/")+1:]
        age = int(imageName[:imageName.find("_")])
        age = (age - ageMin) / (ageMax - ageMin)
        pMatrixXPredict, pMatrixYPredict = prepareDataset(myDll, image, imageW, imageH, 1, component, is255, ageMin, ageMax)
        pVectorXPredict = matrixToVector(myDll, pMatrixXPredict, imageW * imageH * component, 0)
        res = predictPMCRegression(myDll, pArrayWeight, pVectorXPredict, 1, 1)
        age = age * (ageMax - ageMin) + ageMin
        res = res * (ageMax - ageMin) + ageMin
        if display == 1:
            print("age : ", age, "/ predicted : ", res)
        deleteDatasetMatrix(myDll,  pMatrixXPredict, pMatrixYPredict)
        deleteVector(myDll, pVectorXPredict)
        average += (round(res[0]) - age)**2

    average =  average / len(tabSelectedImages)
    return average 

def	predictPMCRegressionAverage(myDll, tabSelectedImages, pArrayWeight, imageW, imageH, component, display, is255):
    average = 0

    for image in tabSelectedImages:
        imageName = image[image.rfind("/")+1:]
        age = int(imageName[:imageName.find("_")])
        pMatrixXPredict, pMatrixYPredict = prepareDataset(myDll, image, imageW, imageH, 1, component, is255, -1, -1)
        pVectorXPredict = matrixToVector(myDll, pMatrixXPredict, imageW * imageH * component, 1)
        res = predictPMCRegression(myDll, pArrayWeight, pVectorXPredict, 1, 1)
        if display == 1:
            print("age : ", age, "/ predicted : ", res)
        deleteDatasetMatrix(myDll,  pMatrixXPredict, pMatrixYPredict)
        deleteVector(myDll, pVectorXPredict)
        average += (round(res[0]) - age)**2
    average =  average / len(tabSelectedImages)
    return average 

def displayPMCRegResult3D(myDll, pArrayWeight, ax, maxRange, lenResult):
    XX, YY, ZZ = [], [], []
    for x1 in range(0, maxRange, 10):
        for x2 in range(0, maxRange, 10):
            x1 /= 100
            x2 /= 100
            XX.append(x1)
            YY.append(x2)
            predictX = np.array([x1, x2])
            datasetTmp = datasetToVector(myDll, predictX, 1)
            value = predictPMCRegression(myDll, pArrayWeight, datasetTmp, 1, lenResult) 
            ZZ.append(value[0])
    ax.plot_trisurf(XX, YY, ZZ, lw=0, color='#bbdefb', alpha=0.5)

def displayPMCRegResult2D(myDll, pPMC, X1, lenResult):
    for x1 in X1:
        predictX = np.array([x1])
        datasetTmp = datasetToVector(myDll, predictX, 1)
        value = predictPMCRegression(myDll, pPMC, datasetTmp, 1, lenResult) 
        plt.scatter(x1, value[0], color='#bbdefb')

def displayPMCClassifResult2DTripleClass(myDll, pPMC, X1, X2, lenResult):
    classA = []
    classB = []
    classC = []

    # Prototyping the method predict PMC 
    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            datasetTmp = datasetToVector(myDll, predictX, 1)
            value = predictPMCClassification(myDll, pPMC, datasetTmp, 1, lenResult)
            if value[0] > value[1] and value[0] > value[2]:
                classA.append(tuple([x1, x2]))
            elif value[1] > value[0] and value[1] > value[2]:
                classB.append(tuple([x1, x2]))
            elif value[2] > value[0] and value[2] > value[1]:
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

def displayPMCClassifResult2D(myDll, pPMC, X1, X2, lenResult):
    classA = []
    classB = []

    # Predict points to test if Model is working 
    for x1 in X1:
        for x2 in X2: 
            predictX = np.array([x1, x2])
            datasetTmp = datasetToVector(myDll, predictX, 1)
            value = predictPMCClassification(myDll, pPMC, datasetTmp, 1, lenResult)
            if value[0] > 0:
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

# Create & Allocate PMC Model using structure (example : [2, 3, 1])
def createPMCModel(myDll, pmcStruct, arrStruct):
    myDll.createPMCModel.argtypes = [ POINTER(ARRAY(c_int, len(pmcStruct))), c_uint ]
    myDll.createPMCModel.restype = c_void_p
    pPMC = myDll.createPMCModel( arrStruct, len(pmcStruct) )
    return pPMC

# Fit PMC with regression version
def fitPMCRegression(myDll, pPMC, pMatrixX, pMatrixY, row, alpha, epochs, display):
    myDll.fitPMCRegression.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_double, c_int, c_int ]
    myDll.fitPMCRegression.restype = c_double								
    error = myDll.fitPMCRegression( pPMC, pMatrixX, pMatrixY, row, alpha, epochs, display )
    return error

# Fit PMC with classification version
def fitPMCClassification(myDll, pPMC, pMatrixX, pMatrixY, row, alpha, epochs, display ):
    myDll.fitPMCClassification.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_double, c_int, c_int ]
    myDll.fitPMCClassification.restype = c_double								
    error = myDll.fitPMCClassification( pPMC, pMatrixX, pMatrixY, row, alpha, epochs, display ) 
    return error

# Predict PMC with classification
def predictPMCClassification(myDll, pPMC, datasetVector, needResult, lenResult):
    myDll.predictPMCClassification.argtypes = [ c_void_p, c_void_p, c_int ]
    myDll.predictPMCClassification.restype = ndpointer(dtype=c_double, shape=(lenResult,))
    result = myDll.predictPMCClassification( pPMC, datasetVector, needResult )
    return result

# Predict PMC with regression
def predictPMCRegression(myDll, pPMC, datasetVector, needResult, lenResult):
    myDll.predictPMCRegression.argtypes = [ c_void_p, c_void_p, c_int]
    myDll.predictPMCRegression.restype = ndpointer(dtype=c_double, shape=(lenResult,))
    result = myDll.predictPMCRegression( pPMC, datasetVector, needResult )
    return result

# Delete / free PMC Model
def deletePMCModel(myDll, pPMC):
    myDll.deletePMCModel.argtypes = [ c_void_p ]
    myDll.deletePMCModel( pPMC )

# Load Weights PMC With CSV
def loadPMCWithCSV(myDll, pathPMC, pPMC):
    #myDll.loadPMCWithCSV.restype = c_void_p 
    myDll.loadPMCWithCSV.argtypes = [ c_char_p, c_void_p ]
    myDll.loadPMCWithCSV( pathPMC.encode('utf-8'), pPMC )

def savePMCInCSV(myDll, pathSavePMC, pPMC):
    myDll.savePMCInCSV.argtypes = [ c_char_p, c_void_p ]
    myDll.savePMCInCSV( pathSavePMC.encode('utf-8'), pPMC )