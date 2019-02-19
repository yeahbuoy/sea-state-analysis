'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.

Taken from https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py
'''

from __future__ import print_function
from apscheduler.schedulers.blocking import BlockingScheduler
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from sklearn.model_selection import train_test_split
from preProcessing import preProcessing
import numpy as np
import datetime
import csv
import time

CSV_DATA_FILE = "../data/CoolSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
fileName = "SoakTestResults.csv"
PICKLE_PATH = "./dataset.pkl"

batch_size = 128
num_classes = 10
epochs = 12

# input image dimensions
img_rows, img_cols = 28, 28

img_rows, img_cols = 270, 480

def LoadAndTest():
    x_data, y_data = preProcessing.load_dataset(IMAGE_DIRECTORY, CSV_DATA_FILE,PICKLE_PATH)

    if K.image_data_format() == 'channels_first':
        x_data = x_data.reshape(x_data.shape[0], 3, img_rows, img_cols)
        input_shape = (3, img_rows, img_cols)

    else:
        x_data = x_data.reshape(x_data.shape[0], img_rows, img_cols, 3)
        input_shape = (img_rows, img_cols, 3)


    x_data = x_data.astype('float32')
    x_data -= np.mean(x_data)
    x_data /= np.std(x_data)
    X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1)
    model = load_model('savedModel.h5')
    score = model.evaluate(X_test, y_test)
    recordResults(score)

def recordResults(score):
    newList = []
    firstRow = ["DateTime","Loss"]
    newList.append(firstRow)
    currList = getRecordedList2D()
    newList += currList
    newRow = [datetime.datetime.now(),score]
    newList.append(newRow)

    myFile = open(fileName, 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(newList)
    myFile.close()



def getRecordedList2D():
    tempList = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            tempRow = []
            if line_count == 0:
                print("")
                line_count += 1
            else:
                if(len(row) != 0):
                    tempRow.append(row[0])  # this will be the datetime
                    tempRow.append(row[1])  # this will be the loss/ results of the test
                    tempList.append(tempRow)
                    line_count += 1

    return tempList

LoadAndTest()
print("results recorded")
time.sleep(5)

