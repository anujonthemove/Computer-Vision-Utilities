import base64
import cv2
import numpy as np
import sys
import coils
import redis
import pickle
import multiprocessing 

cam_name = "cam_"
shape_name = "shape_"

class Writer(object):

	def __init__(self):
		self.__store = redis.Redis()

	def writer(self, video_path, idx):
		
		cap = cv2.VideoCapture(video_path)
		
		# Monitor the framerate at 1s, 5s, 10s intervals.
		fps = coils.RateTicker((1, 5, 10))
		while cap.isOpened():
			ret, frame = cap.read()
			h, w, c = frame.shape
			# reshape or flatten the frame into a string
			res_img = frame.reshape(1, w*h*c)
			# base encode string 
			enc_img = base64.b64encode(res_img).decode("utf-8")
			# store the encoded image against corresponding video/camera name - key-value pairs
			self.__store.set(cam_name+idx, enc_img)
			# store shape of each frame with corresponding camera/video name string
			self.__store.set(shape_name+idx, pickle.dumps((h, w, c)))
			
			cv2.imshow('VIDEO TO REDIS', frame)
			cv2.waitKey(1)
			# Print the framerate.
			text = '{:.2f}, {:.2f}, {:.2f} fps'.format(*fps.tick())
			print(text)


	def run(self):
		
		# video_list = ['/media/anuj/Work-HDD/WORK/CLOUD-DRIVE/Google-Drive/Computer-Vision/Sample-Videos/Slip-And-Fall/test-4.webm', '/media/anuj/Work-HDD/WORK/CLOUD-DRIVE/Google-Drive/Computer-Vision/Sample-Videos/Abandoned-Object/pets2006_1.avi']
		video_list = ['/media/anuj/Work-HDD/WORK/CLOUD-DRIVE/Google-Drive/Computer-Vision/Sample-Videos/RTSP-supported-videos/obama.webm']
		jobs = []
		for i, video_path in enumerate(video_list):
			p = multiprocessing.Process(target=self.writer, args=(video_path, str(i), ))
			p.start()
			jobs.append(p)


		for p in jobs:
			p.join()


		

if __name__ == '__main__':
	obj = Writer()
	obj.run()