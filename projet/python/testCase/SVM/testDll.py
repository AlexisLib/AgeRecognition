from ctypes import *
import matplotlib.pyplot as plt
import numpy as np
import sys

pathDLL = "C:/Users/nico_/Documents/GitHub/ProjetAnnuel3IBD/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"
#pathDLL = "C:/Users/WT57/Documents/ProjetAnnuel3IBD-master/projet/MLAlgorithms/ML_Library/Release/ML_Library.dll"
#pathDLL = "D:/CloudStation/Cours/3IBD/projetAnnuel/projet/MLAlgorithms/ML_Library/x64/Release/ML_Library.dll"

myDll = CDLL(pathDLL)

myDll.testOSQP()