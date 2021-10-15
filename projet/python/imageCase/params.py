from ctypes import *


#### COMMON PARAMS ####

component  = 1
imageW = 100
imageH = 50
numberImageTrain = 1
numberImagePredict = 40
inputCountPerSample = (imageW * imageH * component)
alpha = 0.01
epochs = 10000
display = int(epochs / 10)


#### EVALUATE  ####

startNumberImageTrain = 20
evaluateFactor = 2
numberImagePredictEvaluate = 1388
pathLog = "C:/Users/nico_/Documents/ConvertedImages/EvaluateModels.txt"

##### PMC ####

pmcStruct = [int(inputCountPerSample), 2,  1]
pmcArray = (c_int * len(pmcStruct))(*pmcStruct)
lenPMC = len(pmcStruct)

#### CTYPES ####
c_double_p = POINTER(c_double)

#### SAVE ####
folderSave = "C:/Users/nico_/Documents/ConvertedImages/"
pathSaveLinear = folderSave + "weights_" + str(inputCountPerSample) + "_" + str(imageW) + "_" + str(imageH) + "_" + str(numberImageTrain) + ".csv"
pathSavePMC = folderSave + "weights_PMC_" + str(pmcStruct) + "_" + str(imageW) + "_" + str(imageH) + "_" + str(numberImageTrain) + ".csv"

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
