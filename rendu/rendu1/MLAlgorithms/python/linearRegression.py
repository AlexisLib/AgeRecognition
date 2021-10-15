from ctypes import *
from numpy.ctypeslib import ndpointer
import os
from data import *
from utils import *
from params import *
import random

if __name__ == "__main__":

	#chargemennt de la DLL
	myDll = CDLL(pathDLL)

	imagesPath = os.listdir(pathDataset)
	
	selectedImages = random.sample(imagesPath, numberImage)
	pMatrixX, pMatrixY = prepareDataset(selectedImages, myDll, numberImage)
	
	#changement de dimension pour le transfert
	#arrTrainX, arrTrainXSize = matrixToArray(trainX)

	myDll.create_linear_model.argtypes = [c_int32]
	myDll.create_linear_model.restype = c_void_p
	pArrayWeight = myDll.create_linear_model(inputCountPerSample)

	#entrainement du modèle
	myDll.fit_regression.argtypes = [ 	
										c_void_p,
										c_void_p, 
										c_void_p, 
										c_int,
										c_int 
									]
	myDll.fit_regression.restype = c_double								
	error = myDll.fit_regression	( 	
											pArrayWeight,
											pMatrixX,
											pMatrixY, 
											numberImage,
											inputCountPerSample
										)

	print ("----Prediction---")
	#faire une prediction
	
	toPredictImage = random.sample(imagesPath, 1)
	pMatrixXPredict, pMatrixYPredict = prepareDataset(toPredictImage, myDll, 1)
	myDll.predict_regression.argtypes = [
											c_void_p,
											c_void_p,
											c_int
										]
	myDll.predict_regression.restype = c_double
	predict = myDll.predict_regression	(
											pArrayWeight,
											pMatrixXPredict,
											inputCountPerSample
										)

	print("response : %s , image %s " % (predict, toPredictImage))

	# nettoyage
#myDll.delete_linear_model.argtypes = [ c_void_p ]
#myDll.delete_linear_model( arrayWeight )

