from params import *
import time
from ctypes import *
from numpy.ctypeslib import ndpointer
import os
import sys
from data import *
from utils import *


if __name__ == "__main__":
    start_time = time.time()
    # chargemennt de la DLL
    myDll = CDLL(pathDLL)
    done = 0
    f = open(pathLog, 'a')
    imagesNameTrain = os.listdir(pathDatasetTrain)
    nb = startNumberImageTrain
    while nb <= len(imagesNameTrain):
        f = open(pathLog, 'a')
        selectedImages = random.sample(imagesNameTrain, numberImageTrain)
        selectedImages = convertListToString(selectedImages, pathDatasetTrain)
        pMatrixX, pMatrixY = prepareDataset(selectedImages, myDll, numberImageTrain)

        myDll.createLinearModel.argtypes = [c_int32]
        myDll.createLinearModel.restype = c_void_p
        pArrayWeight = myDll.createLinearModel(inputCountPerSample)
        print ("----Train---")
        myDll.fitLinearRegression.argtypes = [ 	
                                            c_void_p,
                                            c_void_p, 
                                            c_void_p, 
                                            c_int,
                                            c_int 
        ]

        myDll.fitLinearRegression.restype = c_double
        error = myDll.fitLinearRegression	(
                                        pArrayWeight,
                                        pMatrixX,
                                        pMatrixY, 
                                        numberImageTrain,
                                        inputCountPerSample
                                    )
        print ("----Predict---")
        imagesNameTest = os.listdir(pathDatasetPredict)	
        selectedImages = random.sample(imagesNameTest, numberImagePredict)
        selectedImages = [pathDatasetPredict + el for el in selectedImages ]
        
        
        predictResponse = predictAverage(myDll, myDll.predictRegression, selectedImages , pArrayWeight, 30)
        #print("Moyenne erreurs² : %s" % predictResponse )
        f.write("Nombre Image de l'entrainement : %s | W = %s | H = %s \n" % (nb, imageW, imageH))
        f.write("Moyenne erreurs² : %s \n" % predictResponse)
        f.write("Moyenne erreurs : %s \n" % predictResponse**0.5 )
        f.write("--- %s seconds --- \n" % (time.time() - start_time))
        myDll.deleteLinearModel.argtypes = [ c_void_p, c_void_p, c_void_p ]
        myDll.deleteLinearModel( pArrayWeight, pMatrixX, pMatrixY)
        nb = nb * evaluateFactor
        if done == 1:
            break
        if nb > len(imagesNameTrain):
            nb = len(imagesNameTrain)
            done = 1
        f.close()
        print ("----LOG---")
        
    print("--- Evaluate Is OVER ----- \n\n\n\n")
