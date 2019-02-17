'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.

Taken from https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py
'''

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from sklearn.model_selection import train_test_split
from preProcessing import preProcessing
import numpy as np

CSV_DATA_FILE = "../data/CoolSpreadSheet.csv"
IMAGE_DIRECTORY = "../data/Pictures"

batch_size = 128
num_classes = 10
epochs = 12

# input image dimensions
img_rows, img_cols = 28, 28

img_rows, img_cols = 270, 480

x_data, y_data = preProcessing.load_dataset(IMAGE_DIRECTORY, CSV_DATA_FILE)

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
print(score)
'''
model.add(Conv2D(16, kernel_size=(3,3), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(3,3), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='linear'))

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, epochs=5, verbose=1, batch_size=10, validation_data=(X_test, y_test))

predict = model.predict(X_test)
for pred, y in zip(predict, y_test):
    print("Predict: {}\t Actual: {}".format(pred, y))

model.save('savedModel.hd5')

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

# plot_model(model)

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
'''