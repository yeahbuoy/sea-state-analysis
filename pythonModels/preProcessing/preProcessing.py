from PIL import Image
from skimage import io
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os
import unittest
import pickle

def crop_and_split(im):
    im = im.copy()
    cropped = crop_im(im)
    split = split_im(cropped)
    return split


def crop_im(im):
    im = im.copy()
    im = im[0:270]
    return im


def split_im(im):
    im = im.copy()
    sub_images = []
    for i in range(6):
        sub_im = im[:, (i * 480):((i + 1) * 480), :]
        sub_images.append(sub_im)
    return np.asarray(sub_images)


def visible(im):
    if np.median(im) >= 50:
        return True
    else:
        return False



def load_dataframe(path, dataPath, picklePath, outPath, forceNewData = False):
    if os.path.isfile(picklePath) and not forceNewData:
        print("Loading cached dataframe...")
        with open(picklePath, "rb") as pickleFile:
            dataframe = pickle.load(pickleFile)

    else:
        print("Generating new dataframe...")
        dataframe = generate_dataframe(path, dataPath, outPath)
        with open(picklePath, "wb") as pickleFile:
            pickle.dump(dataframe, pickleFile)

    return dataframe


def load_dataset(path, dataPath, picklePath, forceNewData = False):
    if os.path.isfile(picklePath) and not forceNewData:
        print("Loading cached dataset...")
        with open(picklePath, "rb") as pickleFile:
            dataset = pickle.load(pickleFile)

    else:
        print("Generating new dataset...")
        dataset = generate_dataset(path, dataPath)
        with open(picklePath, "wb") as pickleFile:
            pickle.dump(dataset, pickleFile)

    return dataset


def normalize(im):
    #im = im.copy().astype('float16')
    #mean = np.mean(im, axis=(0,1))
    #std = np.std(im, axis=(0,1))
    #im -= mean
    #im /= std
    return im

def generate_dataset(path, dataPath):
    beaufortData = pd.read_csv(dataPath)
    subimages = []
    output = []
    for imagename in os.listdir(path):
        if imagename not in beaufortData['PictureName'].values:
            print("Missing PictureData: {}".format(imagename))
            continue
        imagepath = os.path.join(path, imagename)
        im = io.imread(imagepath)
        if not visible(im):
            continue
        # beaufortNumber = beaufortData.loc[beaufortData['PictureName'] == imagename].iloc[0]['BeaufortForce']
        beaufortNumber = beaufortData.loc[beaufortData['PictureName'] == imagename].iloc[0]['WaveHeight(m)']
        if str(beaufortNumber) == 'nan' or (not (isinstance(beaufortNumber, float) or (isinstance(beaufortNumber, int)))):
            continue

        cropped_and_split = crop_and_split(im)
        normalized = []
        for i in range(len(cropped_and_split)):
            normalized.append(normalize(cropped_and_split[i]))

        subimages.append(normalized)
        for i in range(6):
            output.append(beaufortNumber)

    xdata = np.concatenate(subimages, axis=0)
    ydata = np.asarray(output)
    return xdata, ydata


def generate_dataframe(path, dataPath, outPath):
    rows = []
    beaufortData = pd.read_csv(dataPath, index_col="PictureName")
    for imagename in os.listdir(path):
        if imagename not in beaufortData.index:
            print("Missing PictureData: {}".format(imagename))
            continue
        imagepath = os.path.join(path, imagename)
        im = io.imread(imagepath)
        if not visible(im):
            continue
        df_row = beaufortData.loc[imagename]
        beaufort_number = df_row["BeaufortForce"]
        wind_speed = df_row["WindSpeed(m/s)"]
        wave_height = df_row["WaveHeight(m)"]

        if str(wind_speed) == "nan" or str(wind_speed) == "nan":
            continue

        cropped_and_split = crop_and_split(im)
        normalized = []

        for i in range(len(cropped_and_split)):
            normalized.append(normalize(cropped_and_split[i]))


        for i in range(6):
            subImage_name = "{}_{}.jpg".format(imagename[:-4], i)
            rows.append((subImage_name, beaufort_number, wind_speed, wave_height))
            io.imsave(os.path.join(outPath, subImage_name), normalized[i], plugin="pil", quality=100)

    df = pd.DataFrame.from_records(rows,
                                   columns=["PictureName", "BeaufortNumber", "WindSpeed", "WaveHeight"],
                                   )

    return df




class TestPreProcessingMethods(unittest.TestCase):

    def test_visible(self):
        im = io.imread("../../data/pictures/41001_2016_03_11_1210.jpg")
        self.assertTrue(visible(im), "Visible Image marked Not Visible")

        im = io.imread("../../data/pictures/41001_2016_03_11_0010.jpg")
        self.assertFalse(visible(im), "Dark Image marked Visible")

    def test_split_im(self):
        im = io.imread("../../data/pictures/41001_2016_03_11_1210.jpg")
        subImages = split_im(im)
        self.assertEqual(len(subImages), 6, "Number of Sub Images should be 6")

        for subImage in subImages:
            self.assertEqual(subImage.shape, (im.shape[0], 480, im.shape[2]), "Axis 1 should be of size 480")

        reformed = np.concatenate(subImages, axis=1)
        self.assertTrue(np.array_equal(im, reformed), "Images should be the same of ")


    def test_crop_im(self):
        im = io.imread("../../data/pictures/41001_2016_03_11_1210.jpg")
        cropped = crop_im(im)
        self.assertEqual(cropped.shape, (270, im.shape[1], im.shape[2]), "Axis 0 should be of size 270")
        fakeCropped = im.copy()[0:270, :, :]
        self.assertTrue(np.array_equal(cropped, fakeCropped))

    def test_crop_and_split(self):
        from itertools import combinations
        im = io.imread("../../data/pictures/41001_2016_03_11_1210.jpg")
        result = crop_and_split(im)

        for subImage in result:
            self.assertEqual(subImage.shape, (270, 480, 3), "Axis 1 should be of size 480")

        for a,b in combinations(result, 2):
            self.assertFalse(np.array_equal(a,b), "No two Sub Images should be the same.")

if __name__ == "__main__":
    unittest.main(verbosity=2)

