from PIL import Image
from skimage import io
from skimage.color import rgb2gray
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os
import unittest
import pickle


corruptedFilePath = "./corrupted"

############################################################################# added this method to check for corruption
def is_corrupted(imagePath):
    try:
        img = io.imread(imagePath)
    except:
        return True
    return False

def make_CorruptedDirectory():
    if not os.path.exists(corruptedFilePath):
        os.makedirs(corruptedFilePath)

def moveBadFile(sourceDir, destDir, image):
    ogImage = os.path.join(sourceDir, image)
    newImage = os.path.join(destDir, image)
    os.rename(ogImage,newImage)


def generate_dataframe(path):
    make_CorruptedDirectory()
    goodImages = 0
    badImages = 0
    for imagename in os.listdir(path):
        imagepath = os.path.join(path, imagename)
        if(not is_corrupted(imagepath)):           ############################## this is where I check for corruption
            goodImages += 1
        else:                                           ############################### here's the catch
            print("error opening image: "+ imagepath)
            badImages += 1
            moveBadFile(path,corruptedFilePath,imagename)


    print("badImages: " + str(badImages))
    print("goodImages: " + str(goodImages))



generate_dataframe("./scraped")