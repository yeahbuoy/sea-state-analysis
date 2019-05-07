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
BAD_DEMO = False
BINNED = False

CSV_PATH = "../data/CombinedSpreadSheet.csv"

IMAGE_DIRECTORY = "../data/Pictures"


if BINNED:
    MODEL_PATH = "./savedModels/FinalGreyBin/FinalGreyBucket3.h5"
    PICKLE_PATH = "./savedModels/FinalGreyBin/dataframe.pkl"
else:
    MODEL_PATH = "./savedModels/FinalColorFull/FinalFullColor.h5"
    PICKLE_PATH = "./savedModels/FinalColorFull/dataframeColorFull.pkl"

plt.switch_backend('Qt5Agg')

model = load_model(MODEL_PATH)
data = pd.read_csv(CSV_PATH)

with open(PICKLE_PATH, "rb") as pickleFile:
    training_df = pickle.load(pickleFile)

classes = training_df["BeaufortNumber"].unique()

# Return the real world location of an image
def location(img):
    id = img[0:4]

    locations = {
        "W08A": "EAST HATTERAS - 150 NM East of Cape Hatteras",
        "Z63A": "CANAVERAL EAST - 120NM East of Cape Canaveral",
        "Z24A": "NORTH EQUATORIAL ONE- 470 NM East of Martinique",
        "Z94A": "NORTH EQUATORIAL TWO - 890 NM East of Martinique ",
        "Z09A": "NE ST MARTIN - 330 NM NE St Martin Is",
        "W28A": "NE BAHAMAS - 350 NM ENE of Nassau, Bahamas",
        "Z48A": "WEST BERMUDA - 240 NM West of Bermuda",
        "Z80A": "SOUTH BERMUDA - 300 NM SSE of Bermuda",
        "Z92A": "CORPUS CHRISTI, TX - 60NM SSE of Corpus Christi, TX",
        "Z17A": "GALVESTON,TX -  22 NM East of Galveston, TX",
        "Z71A": "BAY OF CAMPECHE - 214 NM NE of Veracruz",
        "Z41A": "Central Caribbean - 210 NM SSE of Kingston, Jamaica",
        "Z37A": "Eastern Caribbean Sea - 180 NM SSW of Ponce, PR",
        "Z04A": "Caribbean Valley - 63 NM WSW of Montserrat",
        "Z64A": "NANTUCKET SOUND",
        "Z25A": "NY Harbor Entrance - 15 NM SE of Breezy Point , NY",
        "Z76A": "NORTH MICHIGAN - Halfway between North Manitou and Washington Islands.",
        "Z78A": "EAST SUPERIOR - 70 NM NE Marquette, MI",
        "W31A": "SOUTH MICHIGAN - 43NM East Southeast of Milwaukee, WI",
        "W10A": "EAST Lake Ontario  - 20NM North Northeast of Rochester, NY",
        "Z98A": "WEST OREGON - 275NM West of Coos Bay, OR",
        "W04A": "SOUTHEAST PAPA - 600NM West of Eureka, CA",
        "Z23A": "BODEGA BAY - 48NM NW of San Francisco, CA",
        "Z26A": "POINT ARENA - 19NM North of Point Arena, CA",
        "Z08A": "STONEWALL BANK - 20NM West of Newport, OR",
        "Z91A": "EAST SANTA BARBARA  - 12NM Southwest of Santa Barbara, CA",
        "Z57A": "WEST SANTA BARBARA - 38 NM West of Santa Barbara, CA",
        "Z29A": "WEST CALIFORNIA - 357NM West of San Francisco, CA",
        "Z07A": "NW HAWAII ONE - 188 NM NW of Kauai Island, HI",
        "Z59A": "SE HAWAII - 205 NM Southeast of Hilo, HI",
        "Z35A": "NW HAWAII TWO - 186 NM NW of Kauai Is., HI"
    }

    return locations.get(id, "UNKNOWN")

    # if id in locations:
    #     return locations[id]
    # else:
    #     return "UNKNOWN"



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


def plotImages(images, predictions, result, bf, wind, loc):
    if abs(result - bf) <= 1:
        verdict = "Pass"
        if BAD_DEMO:
            return
    else:
        verdict = "Fail"


    loc = loc.split("-")[0].upper()
    fig, axes = plt.subplots(1, 6)
    fig.patch.set_visible(False)
    # fig.suptitle("Wind Speed: {} m/s\nTrue BF: {}\nPredicted BF: {}\nVerdict: {}"\
    #              .format(wind, bf, result, verdict), fontsize=48, ha="right", y=.9)
    fig.text(.50, .97, "Location: \nWind Speed: \nTrue BF: \nPredicted BF: \nVerdict: ",
             fontsize=44, ha="right", va="top")
    fig.text(.50, .97, " {} \n {} m/s\n {}\n {}\n {}" \
            .format(loc, wind, bf, result, verdict), fontsize=44, ha="left", va="top")
    fig.subplots_adjust(top=0.88)
    for i in range(6):
        ax = axes[i]
        ax.imshow(images[i])
        ax.axis("off")
        ax.text(0.5, -0.35, "{}".format(predictions[i]), size=44, ha="center", transform=ax.transAxes)
        ax.set_aspect('equal')
        ax.patch.set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(right=.97, \
                        left=0.03, \
                        bottom=0.0, \
                        top=1, \
                        wspace=.1, \
                        hspace=0)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show(True)

meanScores = []
medianScores = []

numImages = len(data)

data = data.sample(frac=1)
i = 0

if DEMO_PLOT:
    input("Press [Enter] to Continue")
for _, row in data.iterrows():
    i += 1
    if i % 10 == 0:
        print("{} / {}".format(i, numImages))

    pictureName = row["PictureName"]
    bf = int(row["BeaufortForce"])
    wind = row["WindSpeed(m/s)"]
    if wind == "MM":
        print("Bad Image: {}".format(pictureName))
        continue

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

    if DEMO_PLOT and len(normSubImages) == 6 and location(pictureName) != "UNKNOWN":
        plotImages(subImages, predictions, medianScore, bf, wind, location(pictureName))
    elif location(pictureName) == "UNKNOWN":
        print("Unknown Camera Prefix: {}".format(pictureName[0:4]))

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