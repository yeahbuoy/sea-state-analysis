from PIL import Image
from skimage import io
import numpy as np
from matplotlib import pyplot as plt


def crop_and_split(im):
	im = im.copy()
	im = im[0:270,0:2880]
	sub_images = []
	for i in range (6):
		sub_im = im[0: 270, (i*480):((i+1)*480)]
		sub_images.append(sub_im)
		#plt.imshow(sub_im, interpolation='nearest')
	#plt.show()
	return sub_images
	
if __name__ == "__main__":
	#im = Image.open("../data/pictures/41001_2016_03_11_1210.jpg")
	#crop_and_split(im)
	
	im = io.imread("../data/pictures/41001_2016_03_11_1210.jpg")
	crop_and_split_2(im)