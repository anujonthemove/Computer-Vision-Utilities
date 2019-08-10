import cv2
import numpy as np
import os, sys
import shutil

class VideoToVideoWriter(object):
	'''
	Able to write only '.mp4' and '.avi' file formats with currenly installed ffmpeg
	
	'''
	@staticmethod
	def video_writer(path_to_video, video_prefix='video', video_extn='.avi'):


		allowed_vid_extns = ['.avi', '.mp4']
		if video_extn not in allowed_vid_extns:
			print('Unsupported extension, exiting...')
			sys.exit(0)


		# 1. initialize video capture
		cap = cv2.VideoCapture(path_to_video)

		# 2. video properties
		fps = int(cap.get(cv2.CAP_PROP_FPS))
		w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		
		video_name = video_prefix+video_extn
		if video_extn == '.avi':

			# Codec used: MPEG-2 Video (Main Profile)
			# video size in MB is higher than the original 
			out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))

			# Codec used: MPEG-4 Video (Simple Profile) 
			# video size in MB is lower than the original 
			# out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), fps, (w, h))
		elif video_extn == '.mp4':
			out = cv2.VideoWriter(video_name, 0x00000021, fps, (w, h))
			# out = cv2.VideoWriter(video_name, 0x0000006c, fps, (w, h))
		

		while cap.isOpened():

			ret, frame = cap.read()
			
			if ret is True:
				out.write(frame)
				cv2.imshow("Video", frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			else:
				break
					
		cv2.destroyAllWindows()
		cap.release()
		out.release()


def main():
	# Example
	VideoToVideoWriter.video_writer('<path to video>', video_prefix='video', video_extn='.avi')

if __name__ == '__main__':
	main()

