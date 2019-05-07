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
import matplotlib.pyplot as plt

DEMO_PLOT = True

BINNED = False

CSV_PATH = "../data/CombinedSpreadSheet.csv"

CSV_DATA_FILE = "../data/CombinedSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
SPLIT_IMAGE_OUT_PATH = "../data/split_pictures"


if BINNED:
    MODEL_PATH = "./savedModels/FinalGreyBin/FinalGreyBucket3.h5"
    PICKLE_PATH = "./savedModels/FinalGreyBin/dataframe.pkl"
else:
    MODEL_PATH = "./savedModels/FinalColorFull/FinalFullColor.h5"
    PICKLE_PATH = "./savedModels/FinalColorFull/dataframeColorFull.pkl"

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


def plotImages(images, predictions, result, bf):
    fig, axes = plt.subplots(1, 6)
    fig.patch.set_visible(False)
    fig.suptitle("Truth: {}\nPrediction: {}".format(bf, result), fontsize=36)
    fig.subplots_adjust(top=0.88)
    for i in range(6):
        ax = axes[i]
        ax.imshow(images[i])
        ax.axis("off")
        ax.text(0.5, -0.25, "{}".format(predictions[i]), size=24, ha="center", transform=ax.transAxes)
        ax.set_aspect('equal')
        ax.patch.set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show(True)

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

    meanScore = int(np.round(np.mean(predictions)))
    medianScore = int(np.round(np.median(predictions)))

    if DEMO_PLOT and len(normSubImages) == 6:
        plotImages(subImages, predictions, medianScore, bf)

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