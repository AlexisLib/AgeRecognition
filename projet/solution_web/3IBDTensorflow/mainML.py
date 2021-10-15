from utilsImage import *
from frameworkPredict import *
import numpy as np

def getTableResult(pathImg, crop=False):

    results = []
    # Get pixels images
    predictX = np.array(resize_and_get_pixels_from_image(pathImg)).reshape(1, width * height * color)

    # Normalise pixels
    predictX = predictX / (255 * 40000)
    print("HERE", predictX)

    # model Lineare
    myResult = "NA"
    frameworkResult = int(getLinearResultFromFramework(predictX, crop) * 255 * 40000)
    results.append({"nom": "Modele lineaire", "implement": myResult, "framework": frameworkResult})

    # model PMC
    myResult = "NA"
    frameworkResult = int(getPMCResultFromFramework(predictX, crop) * 255 * 40000)
    results.append({"nom": "PMC", "implement": myResult, "framework": frameworkResult})

    results.append({"nom": "RBF", "implement": "NA", "framework": "NA"})
    results.append({"nom": "SVR", "implement": "NA", "framework": "NA"})

    return results

def getMLResults(pathImg, pathImgCrop=None, modele=None):

    print("OCUOUCC")
    print("ICI", pathImg, pathImgCrop)
    results = {"models": None, "modelsHead": None}

    results["models"] = getTableResult(pathImg)

    if pathImgCrop is not None:
        results["modelsHead"] = getTableResult(pathImgCrop, crop=True)


    print(results)


    return results