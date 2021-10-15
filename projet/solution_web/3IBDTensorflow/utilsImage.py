import cv2
import numpy as np
import random
import os
from config import *


def auto_crop_image(image):
    if image is not None:
        im = image.copy()

        # Load HaarCascade from the file with OpenCV
        faceCascade = cv2.CascadeClassifier("ressources/haarcascade_frontalface_default.xml")

        # Read the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        if len(faces) > 0:
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            (x, y, w, h) = faces[0]

            # Crop Image
            if x >= 0 and y >= 0 and w >= 0 and h >= 0:
                crpim = im[y:(y+h), x:(x+w)]
                #crpim = cv2.resize(crpim, (224, 224), interpolation=cv2.INTER_AREA)
            else:
                print("Found {0} faces!".format(len(faces)))

            return crpim, image, (x, y, w, h)
    return None, image, (0, 0, 0, 0)


def get_path_image_clean(path):
    # Ouverture image
    img = cv2.imread(DOSSIER_SAVE + path, color)

    # Decoupage image
    crpimg, imgMod, tmp2 = auto_crop_image(img)

    #Resize Image
    #rescrpimg = cv2.resize( crpimg, (int(200), int(200)) )


    #sauvagarde
    nameImgMod = path[:path.rfind(".")] + "_card" + path[path.rfind("."):]
    cv2.imwrite(DOSSIER_SAVE + nameImgMod, imgMod)

    if crpimg is not None:
        rescrpimg = crpimg
        nameResCropImg = path[:path.rfind(".")] + "_crop" + path[path.rfind("."):]
        cv2.imwrite(DOSSIER_SAVE + nameResCropImg, rescrpimg)

        return nameImgMod, nameResCropImg

    return nameImgMod, None


def get_age_filename(filename):

    try:
        return int(filename.split("_")[0])
    except:
        print("Error nom de l'image : %s" % filename)
        return None


def get_pixels_from_image(path):

    # Gris
    if color == 1:
        cons = cv2.IMREAD_GRAYSCALE

    # Couleurs
    elif color == 3:
        cons = cv2.IMREAD_COLOR

    else:
        raise ValueError("Erreur choix couleur photo")

    img = cv2.imread(path, cons)

    if img.shape[0] == height and img.shape[1] == width:
        return np.array(img).ravel()

    print("Error taille de l'image : %s" % path)
    return None

def resize_and_get_pixels_from_image(path):

    # Gris
    if color == 1:
        cons = cv2.IMREAD_GRAYSCALE

    # Couleurs
    elif color == 3:
        cons = cv2.IMREAD_COLOR

    else:
        raise ValueError("Erreur choix couleur photo")

    print("QQQ", path)
    img = cv2.imread(path, cons)
    img = cv2.resize(img, (width, height))


    if img.shape[0] == height and img.shape[1] == width:
        return np.array(img).ravel()

    print("Error taille de l'image : %s" % path)
    return None


def get_pixels_from_dataset(path, size):

    i = 0
    datasetX = np.empty((0, width * height * color), float)
    datasetY = np.empty((0, 1), float)

    files = os.listdir(path)
    random.shuffle(files)

    for filename in files :
        if i >= size:
            break

        if (i % 100 == 0 and i != 0):
            print("chargement image :", i)
        dataImg = get_pixels_from_image(path + filename)
        ageImg  = get_age_filename(filename)

        if not (dataImg is None or ageImg is None):
            datasetX = np.vstack((datasetX, dataImg))
            datasetY = np.append(datasetY, ageImg)
            # datasetY = np.vstack((datasetY, ageImg))



        i += 1
    return datasetX, datasetY