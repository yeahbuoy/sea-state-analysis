from PIL import Image
from skimage import io
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os

def crop_and_split(im):
	im = im.copy()
	im = im[0:270,0:2880]
	sub_images = []
	for i in range (6):
		sub_im = im[0: 270, (i*480):((i+1)*480)]
		sub_images.append(sub_im)
		#plt.imshow(sub_im, interpolation='nearest')
	#plt.show()
	return np.asarray(sub_images)


def visible(im):
	if np.median(im) >= 50:
		return True
	else:
		return False


def load_dataset(path, dataPath):
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
		beaufortNumber = beaufortData.loc[beaufortData['PictureName'] == imagename].iloc[0]['BeaufortForce']
		for i in range(6):
			output.append(beaufortNumber)
	xdata = np.concatenate(subimages, axis=0)
	return xdata, output






if __name__ == "__main__":
	data = load_dataset("../data/Pictures", "../data/CoolSpreadSheet.csv")

	im = io.imread("../data/pictures/41001_2016_03_11_1210.jpg")
	crop_and_split(im)
	print(visible(im))
	
	im = io.imread("../data/pictures/41001_2016_03_11_0010.jpg")
	crop_and_split(im)
	# should be dark
	print(visible(im))

