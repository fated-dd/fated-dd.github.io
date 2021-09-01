import numpy as np
import cv2
import os

def get_mean_and_std(x):
	x_mean, x_std = cv2.meanStdDev(x)
	x_mean = np.hstack(np.around(x_mean,2))
	x_std = np.hstack(np.around(x_std,2))
	return x_mean, x_std

def advanced_cal():
	source = cv2.imread('static/source/source1.bmp')
	target = cv2.imread('static/target/target1.bmp')
	print("Converting picture...")
	s, t = source , target
	s = cv2.cvtColor(s,cv2.COLOR_BGR2LAB)
	t = cv2.cvtColor(t,cv2.COLOR_BGR2LAB)
	s_mean, s_std = get_mean_and_std(s)
	t_mean, t_std = get_mean_and_std(t)

	height, width, channel = s.shape
	for i in range(0 , height):
		for j in range(0 , width):
			for k in range(0 , channel):
				x = s[i,j,k]
				x = t_mean[k] + ((x - s_mean[k]) * (t_std[k] / s_std[k]))
				# round or +0.5
				x = round(x)
				# boundary check
				x = 0 if x<0 else x
				x = 255 if x>255 else x
				s[i,j,k] = x

	s = cv2.cvtColor(s,cv2.COLOR_LAB2BGR)
	cv2.imwrite('result.bmp' , s)
	cv2.imshow('result.bmp' , s)
	cv2.waitKey(0)


advanced_cal()
os.system("pause")