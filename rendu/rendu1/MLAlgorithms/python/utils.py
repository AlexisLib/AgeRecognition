from ctypes import *
from params import *

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

def convertListToString(list):
	ret = ""
	for el in list:
		ret += pathDataset + el
		ret += ','
	#ret += '\0'
	return ret

def prepareDataset(imagePaths, myDll, numberImage):	
	paths = convertListToString(imagePaths)
	#paths = [x.replace("\\", "/") for x in paths]
	param = paths.encode('utf-8')
	
	myDll.getDatasetX.argtypes = [c_char_p, c_uint, c_uint, c_uint]
	myDll.getDatasetX.restype = c_void_p
	pMatrixX = myDll.getDatasetX(param, sizeImage, numberImage, component)

	myDll.getDatasetY.restype = c_void_p
	myDll.getDatasetY.argtypes = [c_char_p, c_uint]
	pMatrixY = myDll.getDatasetY(param, numberImage)

	return pMatrixX, pMatrixY
