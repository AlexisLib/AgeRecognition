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
	paths = convertListToString(selectedImages)
	paths = [x.replace("\\", "/") for x in paths]
	param = paths.encode('utf-8')
	
	myDll.getDatasetX.argtypes = [ c_char_p , c_uint, c_uint, c_uint ]
	myDll.getDatasetX.restype = [ c_void_p ]
	pMatrixX = myDll.getDatasetX(param, sizeImage, numberImage, 1)

	myDll.getDatasetY.restype = [ c_void_p ]
	myDll.getDatasetY.argtypes = [ c_char_p , c_uint ]
	pMatrixY = myDll.getDatasetY(param, numberImage)
	
	#changement de dimension pour le transfert
	#arrTrainX, arrTrainXSize = matrixToArray(trainX)

	#	myDll.create_linear_model.argtypes = [c_int32]
	#myDll.create_linear_model.restype = c_void_p
	#arrayWeight = myDll.create_linear_model(inputCountPerSample)

	#entrainement du modèle
	myDll.fit_regression.argtypes = [ 	
										#c_void_p,
										POINTER(ARRAY(c_double, arrTrainXSize)), 
										POINTER(ARRAY(c_double, sampleCount)), 
										c_int, c_int 
									]
	myDll.fit_regression.restype = c_double								
	error = myDll.fit_regression	( 	
											#arrayWeight,
											(c_double * arrTrainXSize) (*arrTrainX),
											(c_double * sampleCount) (*trainY), 
											sampleCount, inputCountPerSample
										)

	print ("----Prediction---")
	#print("biais : %s a : %s" % (arrayWeight[0], arrayWeight[1]))
	#faire une prediction
	myDll.predict_regression.argtypes = [
											c_void_p,
											POINTER(ARRAY(c_double, XToPredictSize)),
											c_int
										]
	myDll.predict_regression.restype = c_double
	predict = myDll.predict_regression	(
											arrayWeight,
											(c_double * XToPredictSize) (*XToPredict),
											inputCountPerSample
										)

	print("reponse : %s" % predict)

	# nettoyage
myDll.delete_linear_model.argtypes = [ c_void_p ]
myDll.delete_linear_model( arrayWeight )

