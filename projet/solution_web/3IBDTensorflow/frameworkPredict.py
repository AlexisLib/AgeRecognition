import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import h5py
from utilsImage import *
from keras import backend as K


def getLinearResultFromFramework(predictX, crop):

    print('--------------')
    print(predictX)
    print(predictX.shape)
    print('--------------')


    if crop is True:
        model = load_model(crop_linear_model_framework_to_load)
    else:
        model = load_model(linear_model_framework_to_load)

    value = model.predict(predictX)[0][0]
    K.clear_session()
    return value

def getPMCResultFromFramework(predictX, crop):

    if crop:
        model = load_model(crop_PMC_model_framework_to_load)
    else:
        model = load_model(PMC_model_framework_to_load)
    value = model.predict(predictX)[0][0]
    K.clear_session()
    return value