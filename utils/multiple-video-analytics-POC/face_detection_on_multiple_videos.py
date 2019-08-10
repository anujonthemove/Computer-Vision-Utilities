import cv2 
import numpy as np
import multiprocessing



class FaceDetection(object):
	'''
		Face Detection example showing multiprocessing
	'''
	def __init__(self, video_path):
		self.__video_path = video_path
		print("init done")


	def load_model(self):
		self.__face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
		self.__eye_cascade = cv2.CascadeClassifier('./models/haarcascade_eye.xml') 
		print("models loaded")
 

	def run(self):

		self.load_model()
		cap = cv2.VideoCapture(self.__video_path)
		 
		while True: 
		 
		    # reads frames from a camera
		    ret, img = cap.read() 
		 
		    # convert to gray scale of each frames
		    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		 
		    # Detects faces of different sizes in the input image
		    faces = self.__face_cascade.detectMultiScale(gray, 1.3, 5)
		 
		    for (x,y,w,h) in faces:
		        # To draw a rectangle in a face 
		        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2) 
		        roi_gray = gray[y:y+h, x:x+w]
		        roi_color = img[y:y+h, x:x+w]
		 
		        # Detects eyes of different sizes in the input image
		        eyes = self.__eye_cascade.detectMultiScale(roi_gray) 
		 
		        #To draw a rectangle in eyes
		        for (ex,ey,ew,eh) in eyes:
		            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)
		 
		    # Display an image in a window
		    cv2.imshow('img',img)
		 
		    # Wait for Esc key to stop
		    k = cv2.waitKey(1) & 0xff
		    if k == 27:
		        break
		
		# print "came out of while"
		# Close the window
		cap.release()
		 
		# De-allocate any associated memory usage
		cv2.destroyAllWindows() 


def wrapper(video_path):
	vo = FaceDetection(video_path)
	vo.run()


if __name__ == '__main__':
	
	video_files = ['./test-videos/video-1.avi', './test-videos/video-2.avi', './test-videos/video-3.avi', './test-videos/video-4.avi']
	
	jobs = []
	for idx, video_path in enumerate(video_files):
		p = multiprocessing.Process(target=wrapper, args=(video_path,))
		jobs.append(p)
		p.start()

