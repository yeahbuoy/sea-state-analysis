from keras.models import load_model
import keras
import pandas as pd
import numpy as np
from skimage import io
from preProcessing import preProcessing
import os
from keras_preprocessing.image import ImageDataGenerator


CSV_PATH = "../data/CoolSpreadSheet.csv"

CSV_DATA_FILE = "../data/CoolSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
PICKLE_PATH = "./dataframe.pkl"
SPLIT_IMAGE_OUT_PATH = "../data/split_pictures"

model = load_model("savedModel.h5")
data = pd.read_csv(CSV_PATH, index_col="PictureName")



traindf=preProcessing.load_dataframe(IMAGE_DIRECTORY, CSV_DATA_FILE, PICKLE_PATH, SPLIT_IMAGE_OUT_PATH)
datagen=ImageDataGenerator(preprocessing_function=preProcessing.normalize)

train_generator=datagen.flow_from_dataframe(
    dataframe=traindf,
    directory=SPLIT_IMAGE_OUT_PATH,
    x_col="PictureName",
    #y_col="WaveHeight",
    y_col="BeaufortNumber",
    batch_size=1,
    shuffle=False,
    #class_mode="other",
    class_mode="categorical",
    target_size=(270,480))

# Keras mislabels the classes!!
label_map = train_generator.class_indices
invert_map = dict([[v,k] for k,v in label_map.items()])

#predictions = model.predict_generator(train_generator, train_generator.n)
#predictions = predictions.argmax(axis=-1)

#print(predictions)
#print(traindf["BeaufortNumber"])

#print("done")

#print(model.evaluate_generator(train_generator, steps=train_generator.n, verbose=1))

looseScores = []
tightScores = []
for imageName, row in data.iterrows():
    beaufort_number = row["BeaufortForce"]
    imagePath = os.path.join("../data/pictures", imageName)
    im = io.imread(imagePath)
    splitImages = preProcessing.crop_and_split(im)

    predictions = []
    samples = []
    for subImage in splitImages:
        if preProcessing.is_visible(subImage):
            subImageNorm = preProcessing.normalize(subImage)
            samples.append(subImageNorm)

    if len(samples) > 0:
        X = np.array(samples)
        predictions = model.predict(X)
        predictions = predictions.argmax(axis=-1)
        a=1

    # This is very important!!!
    predictions = [invert_map[p] for p in predictions]

    numPredictions = len(samples)
    if numPredictions > 0:
        medianPrediction = np.median(predictions)
        if medianPrediction != int(medianPrediction):
            meanPrediction = np.mean(predictions)
            if meanPrediction > medianPrediction:
                finalPrediction = int(medianPrediction + 1)
            else:
                finalPrediction = int(medianPrediction)
        else:
            finalPrediction = medianPrediction

        if finalPrediction == beaufort_number:
            tightScores.append(1)
            looseScores.append(1)
        else:
            tightScores.append(0)
            if abs(finalPrediction - beaufort_number) <= 1:
                looseScores.append(1)
            else:
                looseScores.append(0)


        #print("Prediction: {}\tActual: {}\t Samples: {}".format(medianPrediction, beaufort_number, numPredictions))
    else:
        pass
        #print("No sub-image was visible")

print("Tight Accuracy: {}\nLoose Accuracy: {}".format(np.mean(tightScores), np.mean(looseScores)))