import cv2
import numpy as np
import os

def images_to_videos(path_to_images, video_name, fps):
	'''
	# assumes that the imgages are already arranged in a sequence
	'''
	file_list = sorted(os.listdir(path_to_images))
	img = cv2.imread(os.path.join(path_to_images, file_list[0]))
	print(img.shape[:2])
	(height, width) = img.shape[:2]

	out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))

	for file in file_list:
		img = cv2.imread(os.path.join(path_to_images, file))
		cv2.imshow('original', img)
		out.write(img)
		k = cv2.waitKey(1)
		if k == 27:
			cv2.destroyAllWindows()
			break


	out.release()


fps = 30
path_to_images = '/path/to/images/'
video_name = '/path/to/output/video.mp4'

images_to_videos(path_to_images, video_name, fps)