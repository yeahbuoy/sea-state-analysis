from PIL import Image

def crop_and_split(im):
	print(im.size)
	im = im.copy()
	im = im.crop((0, 0, 2880, 270))
	im.show()
	print(im.size)
	
if __name__ == "__main__":
	im = Image.open("../data/pictures/41001_2016_03_11_1210.jpg")
	crop_and_split(im)