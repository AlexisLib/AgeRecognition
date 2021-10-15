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

    X = [1, 0, 0, 1, 0, 0, 1, 1]
    Y = [-1, -1, -1, 1]

    myDll = CDLL(pathDLL)
    
    myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(X))), c_uint, c_uint, c_uint]
    myDll.loadTestCase.restype = c_void_p

    pMatrixX = myDll.loadTestCase((c_double * len(X))(*X), 4, 2, 1)
    myDll.loadTestCase.argtypes = [POINTER(ARRAY(c_double, len(Y))), c_uint, c_uint, c_uint]
    pMatrixY = myDll.loadTestCase((c_double * len(Y))(*Y), 4, 1, 0)

    myDll.createLinearModel.argtypes = [c_int32]
    myDll.createLinearModel.restype = c_void_p
    pArrayWeight = myDll.createLinearModel(2)
    print ("----Train---")
    myDll.fitLinearClassification.argtypes = [ 	
                                        c_void_p,
                                        c_void_p, 
                                        c_void_p, 
                                        c_int,
                                        c_int,
                                        c_double,
                                        c_int
                                        c_int
									]
    myDll.fitLinearClassification.restype = c_double								
    error = myDll.fitLinearClassification	( 	
										    pArrayWeight,
										    pMatrixX,
										    pMatrixY, 
											4,
											2,
                                            0.05,
                                            50,
                                            10
									)
    myDll.saveWeightsInCSV.argtypes = [c_char_p, c_void_p]
    savePath = "C:/Users/nico_/Documents/ConvertedImages/testClassif.csv"
    myDll.saveWeightsInCSV(savePath.encode('utf-8'), pArrayWeight)
	
    myDll.deleteLinearModel.argtypes = [ c_void_p, c_void_p, c_void_p ]
    myDll.deleteLinearModel( pArrayWeight, pMatrixX, pMatrixY)

    # myDll.predictLinearClassification.argtypes = [ c_void_p, c_void_p]
    # myDll.predictLinearClassification.restype = c_double
    # myDll.predictLinearClassification   (W, )
	