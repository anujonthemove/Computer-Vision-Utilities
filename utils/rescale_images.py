import cv2

img = cv2.imread('YOUR_PATH_TO_IMG')

height, width = img.shape[:2]
max_height = 300
max_width = 300

# only shrink if img is bigger than required
if max_height < height or max_width < width:
    # get scaling factor
    scaling_factor = max_height / float(height)
    if max_width/float(width) < scaling_factor:
        scaling_factor = max_width / float(width)
    # resize image
    img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

cv2.imshow("Shrinked image", img)
key = cv2.waitKey()