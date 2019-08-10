import cv2
import numpy as np


def encode_image(img):


	print('Original image shape: ', img.shape)
	_, imenc_img = cv2.imencode('.jpg', img)
	print('Encoded image shape: ', imenc_img.shape)
	return imenc_img



def decode_image(image_np_array):
	
	imdec_img = cv2.imdecode(np.fromstring(image_np_array, dtype=np.uint8), 1)
	print('Decoded image shape:', imdec_img.shape)
	return  imdec_img


path_to_image = '/home/anuj/Pictures/home.jpg'

# read image
img = cv2.imread(path_to_image)	

# encode and flatten
imenc_img = encode_image(img)

# decode and reshape
imdec_img = decode_image(imenc_img)
