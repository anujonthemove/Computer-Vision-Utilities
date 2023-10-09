import os
from PIL import Image
import time
from pprint import pprint

'''
This totally assumes that the images are not already renamed!!! use with caution
'''

path_to_img_dirs = '<path>'
default_extn = ".jpg"


for folder_name in sorted(os.listdir(path_to_img_dirs)):
	print("Processing files in folder: " +str(folder_name))
	files_in_sub_dir = os.listdir(os.path.join(path_to_img_dirs, folder_name))
	
	i = 1
	for file in files_in_sub_dir:
		print("Processing file: " + str(file))
		time.sleep(0.25)
		file_name, extn = os.path.splitext(os.path.basename(file))		
		img_loc = os.path.join(path_to_img_dirs, folder_name)
		img_file_path = os.path.join(img_loc, file)
	
		# convert file to default extension if files are not in it
		if not extn == default_extn:
			print file	
			print("converting file: " +str(img_file_path))
			img = Image.open(img_file_path)
			rgb_img = img.convert('RGB')
			file = file_name+default_extn
			converted_img_path = os.path.join(img_loc, file)
			rgb_img.save(converted_img_path)
			
			print("\n removing file: \n" +str(img_file_path))
			os.remove(img_file_path)
			img_file_path = converted_img_path
			print("UPDATING img_file_path: " + str(img_file_path))
			print("\n NOW IMG img_loc: \n" + str(img_loc))
			time.sleep(5)
		
		num = str(i).zfill(4)
		renamed_file = '%s_%s' % (folder_name, num) + default_extn
		os.rename(img_file_path, os.path.join(img_loc, renamed_file))
		print("File: {} has been renamed to: {}".format(file, renamed_file)) 
		i = i+1
		