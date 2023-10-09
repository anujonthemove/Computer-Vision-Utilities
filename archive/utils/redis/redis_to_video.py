import base64
import cv2
import numpy as np
import sys
import redis
import pickle
import multiprocessing

store = redis.Redis()


class Reader(object):
	def __init__(self):
		self.__store = redis.Redis()

	def reader(self, image_key, shape_key):
		while True:
			enc_img = self.__store.get(image_key)
			enc_img_shape = pickle.loads(self.__store.get(shape_key))

			dec_img = np.frombuffer(base64.decodestring(enc_img), dtype="uint8")
			test_img = dec_img.reshape(enc_img_shape)
			cv2.imshow('REDIS TO VIDEO', test_img)
			cv2.waitKey(1)

	def run(self):
		
		ret_image_keys = ['cam_0']
		ret_shape_keys = ['shape_0']
		
		zipped_list = zip(ret_image_keys, ret_shape_keys)

		jobs = []
		for image_key, shape_key in zipped_list:
			p = multiprocessing.Process(target=self.reader, args=(image_key, shape_key, ))
			p.start()
			jobs.append(p)


		for p in jobs:
			p.join()

if __name__ == '__main__':
	obj = Reader()
	obj.run()