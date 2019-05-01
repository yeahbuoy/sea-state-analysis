from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
#from sklearn.model_selection import train_test_split
from preProcessing import preProcessing
from keras_preprocessing.image import ImageDataGenerator
from models import OurModels
from sklearn.metrics import classification_report, confusion_matrix
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels


import pandas as pd
from keras.utils import plot_model


CSV_DATA_FILE = "../data/SuperCoolSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"
PICKLE_PATH = "./dataframe.pkl"
SPLIT_IMAGE_OUT_PATH = "../data/split_pictures"

batch_size = 128

# input image dimensions
img_rows, img_cols = 28, 28

img_rows, img_cols = 270, 480

def plot_confusion_matrix(classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    arr = [[19039, 102, 341], [687, 2995, 11], [262, 0, 1559]]
    cm = np.array(arr)
    # Only use the labels that appear in the data
    #classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

traindf=preProcessing.load_dataframe(IMAGE_DIRECTORY, CSV_DATA_FILE, PICKLE_PATH, SPLIT_IMAGE_OUT_PATH)
numClasses = traindf["BeaufortNumber"].nunique()

classies = traindf["BeaufortNumber"].unique()
print(classies)
classies2 = []

for x in classies:
    classies2.append(str(x))

datagen=ImageDataGenerator(preprocessing_function=preProcessing.normalize, validation_split=0.25)


test_generator = datagen.flow_from_dataframe(
    dataframe=traindf,
    directory=SPLIT_IMAGE_OUT_PATH,
    x_col="PictureName",
    # y_col="WaveHeight",
    y_col="BeaufortNumber",
    # subset="validation",
    batch_size=1,
    shuffle=False,
    # class_mode="other",
    class_mode="categorical",
    target_size=(270, 480)
)

print("Building Model...")
model = load_model('GreyBucket3.h5')


STEP_SIZE_TEST=test_generator.n//test_generator.batch_size

# Y_pred = model.predict_generator(test_generator, steps=STEP_SIZE_TEST, verbose=1)
# y_pred = np.argmax(Y_pred, axis=1)
# print('Confusion Matrix')
# print(confusion_matrix(test_generator.classes, y_pred))
# print('Classification Report')
#
# print(classification_report(test_generator.classes, y_pred, target_names=classies2))

np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plot_confusion_matrix(classes=["4","1","7"], normalize=True,
                      title='Confusion matrix, without normalization')

plt.show()