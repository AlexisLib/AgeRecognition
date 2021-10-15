from ctypes import *
from numpy.ctypeslib import ndpointer
import os
from data import *
from utils import *
from params import *

if __name__ == "__main__":   

	#chargemennt de la DLL
	myDll = CDLL(pathDLL)

	#changement de dimension pour le transfert
	arrTrainX, arrTrainXSize = matrixToArray(trainX)

	print("---- Création du modèle ----")
	myDll.create_linear_model.argtypes = [c_int32]
	myDll.create_linear_model.restype = c_void_p
	arrayWeight = myDll.create_linear_model(inputCountPerSample)

	print("---- Debut entrainement ----")
	#entrainement du modèle
	myDll.fit_regression_gd.argtypes = [ 	
										c_void_p,
										POINTER(ARRAY(c_double, arrTrainXSize)), 
										POINTER(ARRAY(c_double, sampleCount)), 
										c_int, c_int 
									]
	myDll.fit_regression.restype = c_double								
	error = myDll.fit_regression_gd	( 	
											arrayWeight,
											(c_double * arrTrainXSize) (*arrTrainX),
											(c_double * sampleCount) (*trainY), 
											sampleCount, inputCountPerSample
										)

	print ("\n---- Prediction ----")
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
myDll.delete_linear_model( arrayWeight)

