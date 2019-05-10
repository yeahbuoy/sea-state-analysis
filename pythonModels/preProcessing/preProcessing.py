from PIL import Image
from skimage import io
from skimage.color import rgb2gray
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


def is_dark(im):
    if np.median(im) >= 50:
        return False
    else:
        return True


def is_saturated(im):
    # if np.all(np.percentile(im, 80, axis=(0, 1)) >= 252):  ###############REMOVED BRIGHTNESS FILTER
    #     return True
    # else:
    #     return False
    return False


def is_visible(im):
    if (not is_saturated(im)) and (not is_dark(im)):
        return True
    else:
        return False

############################################################################# added this method to check for corruption
def is_corrupted(imagePath):
    try:
        img = io.imread(imagePath)
    except:
        return True
    return False


def load_dataframe(path, dataPath, picklePath, outPath, forceNewData = False):
    if os.path.isfile(picklePath) and not forceNewData:
        print("Loading cached dataframe...")
        with open(picklePath, "rb") as pickleFile:
            dataframe = pickle.load(pickleFile)

    else:
        print("Generating new dataframe...")
        dataframe = generate_dataframe(path, dataPath, outPath)
        dataframe = dataframe.sample(frac=1)
        with open(picklePath, "wb") as pickleFile:
            pickle.dump(dataframe, pickleFile)

    return dataframe


def normalize(im):
    im = np.array(im, dtype=np.float64)
    im -= np.mean(im, keepdims=True)
    im /= (np.std(im, keepdims=True) + 1e-6)
    return im


def generate_dataframe(path, dataPath, outPath):
    print("Generating DataFrame from {}".format(dataPath))
    rows = []
    beaufortData = pd.read_csv(dataPath, index_col="PictureName", error_bad_lines=False)
    numImages = len(os.listdir(path))
    imageCount = 1
    for imagename in os.listdir(path):
        print("Image {}/{}".format(imageCount, numImages))
        imageCount += 1
        if imagename not in beaufortData.index:
            print("Missing PictureData: {}".format(imagename))
            continue
        imagepath = os.path.join(path, imagename)
        #if(not is_corrupted(imagepath)):           ############################## this is where I check for corruption
        im = io.imread(imagepath)
        df_row = beaufortData.loc[imagename]
        beaufort_number = df_row["BeaufortForce"]
        wind_speed = df_row["WindSpeed(m/s)"]
        #wave_height = df_row["WaveHeight(m)"] ############################### WaveHeight was erroring so just made it one always
        wave_height = 1

        if str(wind_speed) == "nan" or str(wind_speed) == "nan":
            continue

        cropped_and_split = crop_and_split(im)
        normalized = []

        '''
        for i in range(len(cropped_and_split)):
            normalized.append(normalize(cropped_and_split[i]))
        '''

        for i in range(6):
            if not is_visible(cropped_and_split[i]):
                continue
            greyScale = rgb2gray(cropped_and_split[i])
            subImage_name = "{}_{}.jpg".format(imagename[:-4], i)
            rows.append((subImage_name, beaufort_number, wind_speed, wave_height))
            io.imsave(os.path.join(outPath, subImage_name), greyScale, plugin="pil", quality=100)

        '''
        else:                                           ############################### here's the catch
            print("error opening image: "+ imagepath)
        '''

    df = pd.DataFrame.from_records(rows,
                                   columns=["PictureName", "BeaufortNumber", "WindSpeed", "WaveHeight"],
                                   )

    return df




class TestPreProcessingMethods(unittest.TestCase):

    def test_is_dark(self):
        im = io.imread("../../data/pictures/41001_2016_03_11_1210.jpg")
        self.assertFalse(is_dark(im), "Visible Image marked Dark")

        im = io.imread("../../data/pictures/41001_2016_03_11_0010.jpg")
        self.assertTrue(is_dark(im), "Dark Image marked Visible")


    def test_is_saturated(self):
        im = io.imread("../../data/pictures/41001_2016_03_11_2010.jpg")
        subimages = crop_and_split(im)
        self.assertTrue(any([is_saturated(si) for si in subimages]), "Saturated Image marked Not Saturated")

        im = io.imread("../../data/pictures/41001_2016_03_18_1110.jpg")
        subimages = crop_and_split(im)
        self.assertFalse(any([is_saturated(si) for si in subimages]), "NonSaturated Image marked Saturated")


    def test_is_visible(self):
        im = io.imread("../../data/pictures/41001_2016_03_18_1110.jpg")
        subimages = crop_and_split(im)
        self.assertTrue(all([is_visible(si) for si in subimages]), "Visible Image marked Not Visible")

        im = io.imread("../../data/pictures/41001_2016_03_11_0010.jpg")
        subimages = crop_and_split(im)
        self.assertFalse(any([is_visible(si) for si in subimages]), "Dark Image marked Visible")

        im = io.imread("../../data/pictures/41001_2016_03_13_1810.jpg")
        subimages = crop_and_split(im)
        self.assertFalse(is_visible(subimages[1]), "Saturated Image marked Visible")


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

