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

# added this method to check for corruption
def is_corrupted(imagePath):
    try:
        img = io.imread(imagePath)
    except:
        return True
    return False

def makeCorruptedDirectory():
    if not os.path.exists(corruptedFilePath):
        os.makedirs(corruptedFilePath)

def moveBadFile(sourceDir, destDir, image):
    ogImage = os.path.join(sourceDir, image)
    newImage = os.path.join(destDir, image)
    os.rename(ogImage,newImage)

def generate_dataframe(path):
    makeCorruptedDirectory()
    goodImages = 0
    badImages = 0
    for imagename in os.listdir(path):
        imagepath = os.path.join(path, imagename)
        # this is where I check for corruption
        if(not is_corrupted(imagepath)):
            goodImages += 1
        # here's the catch
        else: 
            print("Corrupted image detected: "+ imagepath)
            badImages += 1
            moveBadFile(path,corruptedFilePath,imagename)

    print("badImages: " + str(badImages))
    print("goodImages: " + str(goodImages))

if __name__ == "__main__":
    generate_dataframe("./scraped")