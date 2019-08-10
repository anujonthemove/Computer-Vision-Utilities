import cv2
import numpy as np
import os, sys
import shutil

class VideoToImageWriter(object):


	@staticmethod
	def image_writer(path_to_video, image_prefix='image', image_extn='.jpg', path_to_save=None, zero_pad=4):

		# 1. set defaults
		default_img_dir = './images'

		# 2. check image extension
		allowed_img_extns = ['.jpg', '.jpeg', '.png']
		if image_extn not in allowed_img_extns:
			print('invalid image extension provided, exiting...')
			sys.exit(0)

		extn = image_extn
		image_name = image_prefix

		# 3. set a path to save the images, if none
		if path_to_save is None:
			
			if os.path.exists(default_img_dir):

				try:
					print('default directory already exists, removing it...')
					shutil.rmtree(default_img_dir)

				except OSError as e:
					print("Error: %s - %s." % (e.filename, e.strerror))

			try:
				print('making new {} directory'.format(default_img_dir))
				os.makedirs(default_img_dir)
			except OSError as e:
				print("Error: %s - %s." % (e.filename, e.strerror))			
			
			path_to_save = default_img_dir

		cap = cv2.VideoCapture(path_to_video)

		count = 0
		while cap.isOpened():
			ret, frame = cap.read()
			num = str(count).zfill(zero_pad)
			renamed_file = '%s_%s' % (image_name, num) + extn
			image_path = os.path.join(path_to_save, renamed_file)
			print("writing file: "+ str(image_path))
			cv2.imwrite(image_path, frame)
			count += 1
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			cv2.imshow("Image", frame)
			cv2.waitKey(1)

		cv2.destroyAllWindows()
		cap.release()
		



def main():
	# Example
	VideoToImageWriter.image_writer('/media/anuj/Work-HDD/WORK/CLOUD-DRIVE/Google-Drive/Computer-Vision/Sample-Videos/Abandoned-Object/pets2006_1.avi', image_prefix='image', image_extn='.jpg')

if __name__ == '__main__':
	main()

