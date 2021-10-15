import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from random import *
import h5py
from utilsImage import *

pathDataSet = """C:/dataset/bigdatacrop50x50/"""

#params
nb_epoch = 10000
batch_size = 100
nb_test = 100
input_count_per_sample = width * height * color
name_model = "train_models/PMC_w%s_h%s_c%s_bigdataset.h5" % (width, height, color)
structure = [512, 512, 512, 512, 1]

if __name__ == "__main__":
    #Define the model
    model = Sequential()
    for nb_neuronne in structure[1:-1]:
      model.add(Dense(nb_neuronne, activation = 'tanh', input_dim = input_count_per_sample))
    model.add(Dense(structure[-1], activation = 'linear', input_dim = input_count_per_sample))

    model.compile(optimizer='sgd', loss='mean_squared_error', metrics=['accuracy'])

    for epoch in range(nb_epoch):
        print(epoch)

        datasetX, datasetY = get_pixels_from_dataset(pathDataSet, batch_size)
        datasetX = datasetX / (255 * 40000)
        datasetY = datasetY / (255 * 40000)

        model.fit(datasetX, datasetY, batch_size=batch_size, verbose=0)

        yPredict = np.empty(shape=(0, nb_test))
        yResult = np.empty(shape=(0, nb_test))

        # test
    for i in range(nb_test):
        datasetX, datasetY = get_pixels_from_dataset(pathDataSet, 1)

        datasetX = datasetX / (255 * 40000)
        datasetY = datasetY / (255 * 40000)

        tmpPredict = ((model.predict(datasetX)) * 255 * 40000)[0][0]
        tmpResult = (datasetY * 255 * 40000)[0]

        yPredict = np.append(yPredict, tmpPredict)
        yResult = np.append(yResult, tmpResult)

        # print("Resultat prédiction : ", tmpPredict, "vérité :", tmpResult)

    yPredict = yPredict.flatten()
    yResult = yResult.flatten()
    moy = 0

    for tmpPredict, tmpResult in zip(yPredict, yResult):
        moy += pow((tmpResult - tmpPredict), 2)

    moy = moy / nb_test

    print("Moyenne erreurs² :", moy)
    print("Moyenne erreurs :", pow(moy, 0.5))

    model.save(name_model)