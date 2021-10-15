from ctypes import *
from numpy.ctypeslib import ndpointer
import os
from data import *
from utils import *
import time
from params import *
import random

if __name__ == "__main__":

	start_time = time.time()
	#chargemennt de la DLL
	myDll = CDLL(pathDLL)

	imagesName = os.listdir(pathDatasetTrain)
	
	selectedImages = random.sample(imagesName, numberImageTrain)

	selectedImages = convertListToString(selectedImages, pathDatasetTrain)

	pMatrixX, pMatrixY = prepareDataset(selectedImages, myDll, numberImageTrain)
	
	#changement de dimension pour le transfert
	#arrTrainX, arrTrainXSize = matrixToArray(trainX)

	myDll.loadWeightsWithCSV.argtypes = [c_char_p, c_void_p]
	myDll.loadWeightsWithCSV.restype = c_void_p

	myDll.loadWeightsWithCSV(weights.encode('utf-8'), inputCountPerSample)

	myDll.createLinearModel.argtypes = [c_int32]
	myDll.createLinearModel.restype = c_void_p
	pArrayWeight = myDll.createLinearModel(inputCountPerSample)
	print ("----Train---")
	#entrainement du modèle
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


	#faire une prediction
	
	# for i in range(0, 50):
	# 	print ("----Prediction---")
	# 	toPredictImage = random.sample(imagesName, 1)
	# 	predictResponse = predict(myDll, myDll.predict_regression, toPredictImage, pArrayWeight)
	# 	print("response : %s , image %s \n" % (predictResponse, toPredictImage))
	#
	
	imagesName = os.listdir(pathDatasetPredict)	
	selectedImages = random.sample(imagesName, numberImagePredict)
	selectedImages = [pathDatasetPredict + el for el in selectedImages ]
	#print(selectedImages)

	print ("----Prediction---")
	predictResponse = predictAverage(myDll, myDll.predictLinearRegression, selectedImages , pArrayWeight, 30)
	print("Moyenne erreurs² : %s" % predictResponse )
	print("Moyenne erreurs : %s" % predictResponse**0.5 )

	myDll.saveWeightsInCSV.argtypes = [c_char_p, c_void_p]
	myDll.saveWeightsInCSV(finalSaveWeights.encode('utf-8'), pArrayWeight)
	myDll.deleteLinearModel.argtypes = [ c_void_p, c_void_p, c_void_p ]
	myDll.deleteLinearModel( pArrayWeight, pMatrixX, pMatrixY)
	print("--- %s seconds ---" % (time.time() - start_time))





