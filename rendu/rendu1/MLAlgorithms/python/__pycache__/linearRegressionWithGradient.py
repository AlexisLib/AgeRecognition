from ctypes import *
from numpy.ctypeslib import ndpointer
import os
from data import *
from utils import *
from params import *

if __name__ == "__main__":

	#chargemennt de la DLL
	myDll = CDLL(pathDLL)
	
	#parametrage, initialisation du tableau des poids
	myDll.create_linear_model.argtypes = [c_int]
	myDll.create_linear_model.restype = POINTER(c_double * sizeArrayWeight)
	arrayWeight = myDll.create_linear_model(inputCountPerSample)[0]

	print("Poids : biais=%s a=%s" % (arrayWeight[0], arrayWeight[1]))

	#changement de dimension pour le transfert
	arrTrainX, arrTrainXSize = matrixToArray(trainX)

	#entrainement du modèle
	myDll.fit_regression.argtypes = [ 	
										POINTER(ARRAY(c_double, sizeArrayWeight)),  
										POINTER(ARRAY(c_double, arrTrainXSize)), 
										POINTER(ARRAY(c_double, sampleCount)), 
										c_int, c_int 
									]
	myDll.fit_regression.restype = POINTER(c_double * sizeArrayWeight)									
	arrayWeight = myDll.fit_regression	( 	
											(c_double * sizeArrayWeight) (*arrayWeight), 
											(c_double * arrTrainXSize) (*arrTrainX),
											(c_double * sampleCount) (*trainY), 
											sampleCount, inputCountPerSample
										)[0]

	print ("----Prediction---")
	print("biais : %s a : %s" % (arrayWeight[0], arrayWeight[1]))
	# #faire une prediction
	# myDll.predict_regression.argtypes = [
	# 										POINTER(ARRAY(c_double, sizeArrayWeight)),
	# 										POINTER(ARRAY(c_double, XToPredictSize)),
	# 										c_int
	# 									]
	# myDll.predict_regression.restype = c_double
	# predict = myDll.predict_regression	(
	# 										(c_double * sizeArrayWeight) (*arrayWeight),
	# 										(c_double * XToPredictSize) (*XToPredict),
	# 										inputCountPerSample
	# 									)

	# print("reponse : %s" % predict)

# 	# nettoyage
# myDll.delete_linear_model.argtypes = [ POINTER(ARRAY(c_double, sizeArrayWeight)) ]
# myDll.delete_linear_model( (c_double * sizeArrayWeight)(*arrayWeight) )

