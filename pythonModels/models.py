from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras import metrics
from sklearn.model_selection import train_test_split
from preProcessing import preProcessing


class OurModels:

    @staticmethod
    def george_1(input_shape):
        model = Sequential()
        model.add(Conv2D(4, kernel_size=(16, 16), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(8, kernel_size=(8, 8), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(16, kernel_size=(4, 4), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(16, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(4, activation='relu'))
        model.add(Dense(1, activation='linear'))

        model.compile(loss='mean_squared_error', optimizer='adam')

        return model


    @staticmethod
    def george_categorical(input_shape):
        model = Sequential()
        model.add(Conv2D(4, kernel_size=(9, 9), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(8, kernel_size=(9, 9), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(16, kernel_size=(9, 9), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(11, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[metrics.categorical_accuracy])

        return model


    @staticmethod
    def casey_model():
        pass

    @staticmethod
    def alex_model():
        model = Sequential()
        model.add(Conv2D(4, kernel_size=(16, 16), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(8, kernel_size=(8, 8), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(16, kernel_size=(4, 4), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(11, activation='softmax'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        return model

    @staticmethod
    def alex_model2():
        model = Sequential()
        model.add(Conv2D(4, kernel_size=(16, 16), activation='softmax', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(8, kernel_size=(8, 8), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(16, kernel_size=(4, 4), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(11, activation='softmax'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        return model
