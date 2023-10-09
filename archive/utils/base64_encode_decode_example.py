import cv2
import numpy as np
import base64
import time

'''
Refer this: https://stackoverflow.com/questions/45923296/convert-base64-string-to-an-image-thats-compatible-with-opencv?rq=1 

'''


def base64_encode_decode_example(img):

	w, h, c = img.shape
	print('Original image shape: ', (w, h, c))

	img_dtype = img.dtype
	print('Original image dtype: ', img_dtype)
	
	reshaped_org_img = img.reshape(1, w*h*c)

	# encode 
	enc_img = base64.b64encode(reshaped_org_img)
	# .decode("utf-8")

	# decode 
	dec_img = np.frombuffer(base64.decodestring(enc_img), dtype=img_dtype)
	
	# reshape
	reshaped_dec_img = dec_img.reshape(w, h, c)
	 
	print(reshaped_dec_img.shape)

	cv2.imshow('reshaped_dec_img', reshaped_dec_img)
	cv2.waitKey()



path_to_img = 'home.jpg'
img = cv2.imread(path_to_img)

base64_encode_decode_example(img)
