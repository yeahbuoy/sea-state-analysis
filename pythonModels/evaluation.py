from keras.models import load_model
import keras
import pandas as pd
import numpy as np
from skimage import io
from preProcessing import preProcessing
import os
import pickle
from keras_preprocessing.image import ImageDataGenerator
from skimage.color import rgb2gray


CSV_PATH = "../data/CombinedSpreadSheet.csv"

CSV_DATA_FILE = "../data/CombinedSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
PICKLE_PATH = "./savedModels/FinalGreyBin/dataframe.pkl"
SPLIT_IMAGE_OUT_PATH = "../data/split_pictures"

MODEL_PATH = "./savedModels/FinalGreyBin/FinalGreyBucket3.h5"

model = load_model(MODEL_PATH)
data = pd.read_csv(CSV_PATH)

with open(PICKLE_PATH, "rb") as pickleFile:
    training_df = pickle.load(pickleFile)

classes = training_df["BeaufortNumber"].unique()


def norm(imgs):
    newImgs = []
    for img in imgs:
        if preProcessing.is_visible(img):
            normImg = rgb2gray(img)
            normImg = np.dstack((normImg, normImg, normImg))
            normImg = preProcessing.normalize(normImg)
            newImgs.append(normImg)
        # else:
        #     newImgs.append(None)
    return newImgs


meanScores = []
medianScores = []

numImages = len(data)

data = data.sample(frac=1)
i = 0
for _, row in data.iterrows():
    i += 1
    if i % 10 == 0:
        print("{} / {}".format(i, numImages))


    pictureName = row["PictureName"]
    bf = int(row["BeaufortForce"])

    imagePath = os.path.join(IMAGE_DIRECTORY, pictureName)

    if os.path.isfile(imagePath):
        compositeImage = io.imread(imagePath)
    else:
        continue

    subImages = preProcessing.crop_and_split(compositeImage)

    normSubImages = norm(subImages)

    if len(normSubImages):
        X = np.array(normSubImages)
        predictions = model.predict(X).argmax(axis=-1)
        predictions = [classes[x] for x in predictions]

    else:
        continue

    meanScore = np.round(np.mean(predictions))
    medianScore = np.round(np.median(predictions))

    if abs(bf - meanScore) <= 1:
        meanScores.append(1)
    else:
        meanScores.append(0)

    if abs(bf - medianScore) <= 1:
        medianScores.append(1)
    else:
        medianScores.append(0)


meanGrandScore = np.mean(meanScores)
medianGrandScore = np.mean(medianScores)
print("Mean of Votes Accuracy: {}".format(meanGrandScore))
print("Median of Votes Accuracy: {}".format(medianGrandScore))