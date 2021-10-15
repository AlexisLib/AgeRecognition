from numpy.ctypeslib import ndpointer
import os
from data import *
from utils import *
from params import *
import random

if __name__ == "__main__":
    myDll = CDLL(pathDLL)
    imagesPath = os.listdir(pathDataset) #// remplacer \ par /
    selectedImages = random.sample(imagesPath, 50)
    selectedImages = [x.replace("\\", "/") for x in  selectedImages]
    paths = convertListToString(selectedImages)
    # imagesPathFinal = matrixToArray(imagesPath)
    param = paths.encode('utf-8')
    myDll.getDatasetX.argtypes = [ c_char_p , c_uint, c_uint, c_uint ]
      #myDll.getDatasetX.restype = [ ]
    myDll.getDatasetX(param, sizeImage, 3, 1)

    myDll.getDatasetY.argtypes = [ c_char_p , c_uint ]
    myDll.getDatasetY(param, 3)