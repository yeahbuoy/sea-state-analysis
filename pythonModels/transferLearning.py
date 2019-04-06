
import pandas as pd
import numpy as np
import os
import keras
import matplotlib.pyplot as plt
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras import metrics
from preProcessing import preProcessing
from keras.optimizers import Adam

CSV_DATA_FILE = "../data/CoolSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
PICKLE_PATH = "./dataframe.pkl"
SPLIT_IMAGE_OUT_PATH = "../data/split_pictures"

batch_size = 128
num_classes = 10
epochs = 50

# input image dimensions
img_rows, img_cols = 28, 28

img_rows, img_cols = 270, 480



base_model=MobileNet(weights='imagenet',include_top=False) #imports the mobilenet model and discards the last 1000 neuron layer.

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x) #we add dense layers so that the model can learn more complex functions and classify for better results.
x=Dense(1024,activation='relu')(x) #dense layer 2
x=Dense(512,activation='relu')(x) #dense layer 3
preds=Dense(11,activation='softmax')(x) #final layer with softmax activation


model=Model(inputs=base_model.input,outputs=preds)
#specify the inputs
#specify the outputs
#now a model has been created based on our architecture


## simply for checking layers, comment out as needed
# for i,layer in enumerate(model.layers):
#   print(i,layer.name)


for layer in model.layers:
    layer.trainable=False
## or if we want to set the first 20 layers of the network to be non-trainable
for layer in model.layers[:20]:
    layer.trainable=False
for layer in model.layers[20:]:
    layer.trainable=True


##preprocessing

# train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) #included in our dependencies
#
# train_generator=train_datagen.flow_from_directory('path-to-the-main-data-folder',
#                                                  target_size=(224,224),
#                                                  color_mode='rgb',
#                                                  batch_size=32,
#                                                  class_mode='categorical',
#                                                  shuffle=True)


traindf=preProcessing.load_dataframe(IMAGE_DIRECTORY, CSV_DATA_FILE, PICKLE_PATH, SPLIT_IMAGE_OUT_PATH)
# shuffles the dataframe
traindf = traindf.sample(frac=1)
datagen=ImageDataGenerator(preprocessing_function=preProcessing.normalize, validation_split=0.25)
train_generator=datagen.flow_from_dataframe(
    dataframe=traindf,
    directory=SPLIT_IMAGE_OUT_PATH,
    x_col="PictureName",
    #y_col="WaveHeight",
    y_col="BeaufortNumber",
    subset="training",
    batch_size=13,
    shuffle=True,
    #class_mode="other",
    class_mode="categorical",
    target_size=(270,480))

validation_generator=datagen.flow_from_dataframe(
    dataframe=traindf,
    directory=SPLIT_IMAGE_OUT_PATH,
    x_col="PictureName",
    #y_col="WaveHeight",
    y_col="BeaufortNumber",
    subset="validation",
    batch_size=13,
    shuffle=True,
    #class_mode="other",
    class_mode="categorical",
    target_size=(270,480)
)


model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=[metrics.categorical_accuracy])
# Adam optimizer
# loss function will be categorical cross entropy
# evaluation metric will be accuracy

print("Fitting Model...")
#model.fit(X_train, y_train, epochs=5, verbose=1, batch_size=10, validation_data=(X_test, y_test))

STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
STEP_SIZE_TEST=validation_generator.n//validation_generator.batch_size
model.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    epochs=epochs,
                    verbose=1,
                    validation_data=validation_generator,
                    validation_steps=STEP_SIZE_TEST)