from PIL import Image

def crop_and_split(im):
	#print(im.size)
	im = im.copy()
	im = im.crop((0, 0, 2880, 270))
	#im.show()
	sub_images = []
	for i in range (6):
		sub_im = im.crop((i * 480, 0, (i+1) * 480, 270))
		#sub_im.show()
		sub_images.append(sub_im)
		#print(sub_im.size)
	return sub_images
	
if __name__ == "__main__":
	im = Image.open("../data/pictures/41001_2016_03_11_1210.jpg")
	crop_and_split(im)