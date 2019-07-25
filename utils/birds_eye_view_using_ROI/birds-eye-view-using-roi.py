import numpy as np
import cv2
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'roi_selector')))
# this is a huge chunk of code with 
# a lot of functionality therefore, kept separate
import draw_custom_roi


def select_roi(frame):
	"""
	select roi in order 
	top-left, top-right, bottom-right, bottom-left
	"""
	copy_frame = frame.copy()
	pts = draw_custom_roi.define_roi(frame, copy_frame)
	print("selected coordinates: ", pts)
	return np.array(pts, dtype=np.float32)


def four_point_transform(image, pts):
	'''
	* code taken from pyimage search blog
	* we have modified it slightly though for our usage
	'''
	rect = pts
	(tl, tr, br, bl) = rect

	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	# return the warped image
	return warped


def main():

	# read image
	img = cv2.imread('arco-center-ice.jpg')

	# resize, if needed
	# img = cv2.resize(img, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_CUBIC)
	# img = cv2.resize(img, (640, 480), interpolation = cv2.INTER_CUBIC)

	pts = select_roi(img)
	print(pts)

	warped_im = four_point_transform(img, pts)

	cv2.imshow('test', warped_im)
	cv2.imwrite('test.png', warped_im)
	k = cv2.waitKey()
	if k == 27:
		cv2.destroyAllWindows()

	print('End of Demo! Thanks!')



if __name__ == "__main__":
	main()