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

def visible(im):
	if np.median(im) >= 50:
		return True
	else:
		return False

if __name__ == "__main__":
	im = io.imread("../data/pictures/41001_2016_03_11_1210.jpg")
	crop_and_split(im)
	print(visible(im))
	
	im = io.imread("../data/pictures/41001_2016_03_11_0010.jpg")
	crop_and_split(im)
	# should be dark
	print(visible(im))