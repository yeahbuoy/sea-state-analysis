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
        subimages.append(crop_and_split(im))
        # beaufortNumber = beaufortData.loc[beaufortData['PictureName'] == imagename].iloc[0]['BeaufortForce']
        beaufortNumber = beaufortData.loc[beaufortData['PictureName'] == imagename].iloc[0]['WindSpeed(m/s)']
        for i in range(6):
            output.append(beaufortNumber)
    xdata = np.concatenate(subimages, axis=0)
    ydata = np.asarray(output)
    return xdata, ydata


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
    unittest.main()

