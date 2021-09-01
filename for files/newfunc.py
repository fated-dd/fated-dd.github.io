import numpy as np
import cv2
from sympy import Eq , symbols , solve
import statistics
import time



s = cv2.imread('source/source12.bmp')
sstore = s
t = cv2.imread('target/target1.bmp')
tstore = t

s_height , s_width , s_vac = s.shape
t_height , t_width , t_vac = t.shape

if s_height < t_height:
    height_option = 0
else:
    height_option = 1

if s_width < t_width:
    width_option = 0
else:
    width_option = 1

height_list = [s_height , t_height]
width_list = [s_width , t_width]

# print(s)
# print(s_height , s_width , s_vac)
# print(t_height , t_width , t_vac)
# print(height_option , width_option)
# print(height_list[height_option])
# print(width_list[width_option])
# print(s[2 , 3 , 2] , s[2][3][2])
def one_to_one_cal():
    s_copy = s
    for i in range(100):
        for o in range(100):
            for p in range(s_vac):
                pixel = s[i][o][p]
                target_pixel = t[i][o][p]
                times = 0
                for b in range(-5 , 5):
                    for c in range(-5 , 5):
                        iround = i+b
                        oround = o+c
                        if iround < 0:
                            iround = 0
                        if oround < 0:
                            oround = 0
                        if iround >= height_list[height_option]:
                            iround = height_list[height_option]-1
                        if oround >= width_list[width_option]:
                            oround = width_list[width_option] -1
                        target_pixel += t[iround][oround][p]
                        times+=1
                target_pixel = target_pixel/times
                newpixel = 0.5*pixel+0.5*target_pixel
                s_copy[i][o][p] = newpixel
    
    cv2.imshow('result' , s_copy)
    cv2.waitKey(0)

one_to_one_cal()