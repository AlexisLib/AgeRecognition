from ctypes import *
import os
from data import *
from utils import *
import time
from params import *
import random
import numpy as np
import matplotlib.pyplot as plt
from numpy.ctypeslib import ndpointer

if __name__ == "__main__":

    myDll = CDLL(pathDLL)

    # Select randomly X Images from the training dataset.
    imagesName = os.listdir(pathDatasetTrain)
    selectedImages = random.sample(imagesName, numberImageTrain)
    selectedImages = convertListToString(selectedImages, pathDatasetTrain)

    # Load selected images in Matrix (with OPENCV)
    pMatrixX, pMatrixY = prepareDataset(selectedImages, myDll, numberImageTrain)

    # Create & Allocate PMC Model using pmcStruct (located in params.py)
    myDll.createPMCModel.argtypes = [ POINTER(ARRAY(c_int, len(pmcStruct))), c_uint ]
    myDll.createPMCModel.restype = c_void_p
    pArrayWeight = myDll.createPMCModel(pmcArray, len(pmcStruct))

    # Fit PMC with regression version
    myDll.fitPMCRegression.argtypes = [ c_void_p, c_void_p, c_void_p, c_int, c_double, c_int, c_int ]
    myDll.fitPMCRegression.restype = c_double								
    error = myDll.fitPMCRegression( pArrayWeight, pMatrixX, pMatrixY, numberImageTrain,  alpha, epochs, display)

    # Save PMC
    # myDll.savePMCInCSV.argtypes = [c_char_p, c_void_p]
    # myDll.savePMCInCSV(pathSavePMC.encode('utf-8'), pArrayWeight)
    
    # # Load PMC
    # wload = "C:/Users/nico_/Documents/ConvertedImages/weights_PMC_[5000, 2, 1]_100_50_1.csv"
    # myDll.loadPMCWithCSV.argtypes = [ c_char_p ]
    # myDll.loadPMCWithCSV(wload.encode('utf-8'))

    # #Select randomly X Images from the Predict dataset.
    imagesName = os.listdir(pathDatasetPredict)	
    selectedImages = random.sample(imagesName, numberImagePredict)
    selectedImages = [pathDatasetPredict + el for el in selectedImages ]


    print ("----Prediction---")
    predictResponse = predictPMCRegressionAverage(myDll, myDll.predictPMC, selectedImages , pArrayWeight)
    print("Moyenne erreurs² : %s" % predictResponse )
    print("Moyenne erreurs : %s" % predictResponse**0.5 )
    myDll.deletePMCModel.argtypes = [ c_void_p ]
    myDll.deletePMCModel( pArrayWeight )



 
	







 
