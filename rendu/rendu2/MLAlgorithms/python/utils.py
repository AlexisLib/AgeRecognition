from ctypes import *
from params import *
import os
import random

def printRes(tab):
	for el in tab:
		print (el)

def truncate(n, size):
	return float(str(n)[:size+2])

def matrixToArray(matrix):
	ret = []
	for el in matrix:
		ret.extend(el)
	return ret, len(ret)

def convertListToString(myList, path):
	ret = ""
	for el in myList:
		ret += path + el
		ret += ','
	return ret

def prepareDataset(imagePaths, myDll, numberImage):	
	param = imagePaths.encode('utf-8')
	myDll.getDatasetX.argtypes = [c_char_p, c_uint, c_uint, c_uint, c_uint]
	myDll.getDatasetX.restype = c_void_p
	pMatrixX = myDll.getDatasetX(param, imageW, imageH, numberImage, component)

	myDll.getDatasetY.restype = c_void_p
	myDll.getDatasetY.argtypes = [c_char_p, c_uint]
	pMatrixY = myDll.getDatasetY(param, numberImage)

	return pMatrixX, pMatrixY

#tester
def predict(myDll, function, path, pArrayWeight):
	pMatrixXPredict, pMatrixYPredict = prepareDataset(path, myDll, 1)
	function.argtypes = [
							c_void_p,
							c_void_p,
						]
	function.restype = c_double
	predictResponse = function (
							pArrayWeight,
							pMatrixXPredict
						)
	myDll.deleteTmpPredict.argtypes =  [ c_void_p, c_void_p ]
	myDll.deleteTmpPredict ( pMatrixXPredict, pMatrixYPredict )

	return predictResponse

def	predictAverage(myDll, function, tabSelectedImages, pArrayWeight):
	average = 0
	
	for image in tabSelectedImages:
		imageName = image[image.rfind("/")+1:]
		age = int(imageName[:imageName.find("_")])
		res = predict(myDll, function, image, pArrayWeight)
		average += (round(res) - age)**2
		
	average =  average / len(tabSelectedImages)
	return average 
	



