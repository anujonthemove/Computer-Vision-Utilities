import multiprocessing
import cv2
import time
import os

def detect_faces(records, name, result_list):

	face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')

	count = 0
	while True:

		sub_l = manager.list(result_list[0])


		# analytics_obj_dict = {}
		# time.sleep(2)
		if len(records)  > 0:
			
			frame = records[-1]
			# convert to gray scale of each frames
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# Detects faces of different sizes in the input image
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)

			object_str = 'face_'
			object_dict = {}
			# print(faces)
			for idx, (x,y,w,h) in enumerate(faces):
				# print("inside detection: ", faces[0])
				# To draw a rectangle in a face 
				object_dict[object_str+str(idx)] = [faces[0].tolist()]
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2) 
				roi_gray = gray[y:y+h, x:x+w]
				roi_color = frame[y:y+h, x:x+w]


			# print(object_dict)

			# analytics_obj_dict[name] = object_dict 
				# Detects eyes of different sizes in the input image
				# eyes = eye_cascade.detectMultiScale(roi_gray) 

				#To draw a rectangle in eyes
				# for (ex,ey,ew,eh) in eyes:
					# cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)

			# Display an image in a window
			# print(analytics_obj_dict)
			sub_l.append((name, object_dict))
			# print("len subl: ", len(sub_l))

			result_list[0] = sub_l

			if len(result_list[0]) > 150:
				# print("IT WAS GREATER")
				sub_l.pop(0)

			# print("len result_list: ", len((result_list[0])))
			# print("from insert: ", result_list[0])

			count += 1
			cv2.imshow(name, frame)


			k = cv2.waitKey(1)
			if k == 27:
				cv2.destroyAllWindows()
				break
			
		else:
			print("No images present")
			cv2.destroyAllWindows()



# def detect_eyes(records, name):

# 	face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
# 	eye_cascade = cv2.CascadeClassifier('./models/haarcascade_eye.xml')

# 	while True:
		
# 		if len(records)  > 0:
			
# 			frame = records[-1]
# 			# convert to gray scale of each frames
# 			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 			# Detects faces of different sizes in the input image
# 			faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# 			for (x,y,w,h) in faces:
# 				# To draw a rectangle in a face 
# 				# cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2) 
# 				roi_gray = gray[y:y+h, x:x+w]
# 				roi_color = frame[y:y+h, x:x+w]

# 				# Detects eyes of different sizes in the input image
# 				eyes = eye_cascade.detectMultiScale(roi_gray) 

# 				#To draw a rectangle in eyes
# 				for (ex,ey,ew,eh) in eyes:
# 					cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)

# 			# Display an image in a window
# 			cv2.imshow(name, frame)


# 			k = cv2.waitKey(1)
# 			if k == 27:
# 				cv2.destroyAllWindows()
# 				break
			
# 		else:
# 			print("No images present")
# 			cv2.destroyAllWindows()



def print_records(records, result_list, name):

	while True:
		# time.sleep(2)
		if len(records)  > 0 and len(result_list[0]) > 0:
			frame = records[-1]
			# print(len(result_list[0]))
			# print(result_list[0][-1][name])

			# faces = None
			
			last_elm = result_list[0]
			# print(result_list[0])
			_, val = last_elm[-1]

			for idx, (key, value) in enumerate(val.items()):
				print("times: ", idx)
				faces = value
				# print('faces: ', faces, result_list[0])

				# # print("inside final: ", type(faces))
				for (x,y,w,h) in faces:
				# 	# To draw a rectangle in a face 
					cv2.rectangle(frame, (x,y),(x+w,y+h),(255,255,0),2)

			if len(val.items()) > 1:
				print('IT WAS GREATER HERE ##################')
				print("DEBUG: ", val.items())

				cv2.imwrite('test.jpg', frame)
			
			cv2.imshow("inside_print_record", frame)

			k = cv2.waitKey(10)
			if k == 27:
				cv2.destroyAllWindows()
				break
			
		else:
			print("No images present in print records")
			cv2.destroyAllWindows()



def check_result(result_list, q):

	while q.get() is not 'DONE':
		time.sleep(2)
		# if q.get() == 'DONE':
		# 	print('IT WAS DONE, SHOULD BE KILLED')
		# 	break
		print("Queue: ", q.get())
		# print(len(result_list))
		# print("from print: ",result_list[0])
	print('GOT KILLED')



def insert_record(records, q):
	
	# print(os.getpid())
	video_path = '/media/anuj/Work-HDD/WORK/CLOUD-DRIVE/Google-Drive/Computer-Vision/Sample-Videos/RTSP-supported-videos/obama.webm'
	cap = cv2.VideoCapture(video_path)

	count = 0
	q.put('STARTED')
	while True:
		# time.sleep(2)
		ret, frame = cap.read()
		records.append(frame.copy())
		
		if len(records) > 150:
			records.pop(0)
		cv2.imshow("inside_insert_record", frame)
		count += 1
		k = cv2.waitKey(1)
		if k == 27:
			break
			cap.release()
			cv2.destroyAllWindows()
			q.put('DONE')

	q.put('DONE')

	cap.release()
	cv2.destroyAllWindows()





if __name__ == '__main__':

	
	with multiprocessing.Manager() as manager:
		# creating a list in server process memory
		records = manager.list([])
		
		result_list = manager.list([[], []])
		# result_list = manager.list([[], []])

		q = multiprocessing.Queue()

		process_list = []

		# creating new processes
		p1 = multiprocessing.Process(target=insert_record, args=(records, q, ))
		p1.daemon = True
		p1.start()

		# process_list.append(p1)
		
		p2 = multiprocessing.Process(target=detect_faces, args=(records, "face_det_1", result_list))
		p2.start()

		# process_list.append(p2)

		# p3 = multiprocessing.Process(target=detect_eyes, args=(records, "eyes-1"))
		# p3.start()

		# p4 = multiprocessing.Process(target=detect_eyes, args=(records, "eyes-2"))
		# p4.start()

		# p5 = multiprocessing.Process(target=check_result, args=(result_list, q))
		# p5.start()

		p6 = multiprocessing.Process(target=print_records, args=(records, result_list, 'face_det_1'))
		p6.start()

		# process_list.append(p6)


		# for p in process_list:
			# p.join()
		p1.join()
		p2.join()
		# p3.join()
		# p4.join()
		# p5.join()
		p6.join()

		



