from ctypes import *


#### COMMON PARAMS ####

component  = 1
imageW = 100
imageH = 50
numberImageTrain = 400
numberImagePredict = 40
inputCountPerSample = (imageW * imageH * component)

#### SAVE ####
pathSaveWeights = "C:/Users/nico_/Documents/ConvertedImages/"
finalSaveWeights = pathSaveWeights + "weights_" + str(inputCountPerSample) + "_" + str(imageW) + "_" + str(imageH) + "_" + str(numberImageTrain) + ".csv"

#### EVALUATE  ####

startNumberImageTrain = 20
evaluateFactor = 2
numberImagePredictEvaluate = 1388
pathLog = "C:/Users/nico_/Documents/ConvertedImages/EvaluateModels.txt"

##### PMC ####

pmcStruct = [1]
arrStruct = (c_int * len(pmcStruct))(*pmcStruct)

#### CTYPES ####
c_double_p = POINTER(c_double)

#### DLL PATHS ####
#nico
pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

#tatane
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Debug/ML_Library.dll

#### DATASET PATHS ####

#nico
pathDatasetTrain = "C:/Users/nico_/Documents/ConvertedImages/SplittedMinus/train/"
pathDatasetPredict = "C:/Users/nico_/Documents/ConvertedImages/SplittedMinus/test/"

#tatane
#pathDatasetTrain = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/dataset/minusLotte/"
#pathDatasetPredict = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/dataset/minusLotte/"
