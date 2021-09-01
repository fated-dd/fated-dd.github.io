import numpy as np
import cv2
from sympy import Eq , symbols , solve
import statistics

s = cv2.imread('Program/source/source12.bmp')
sstore = s
t = cv2.imread('Program/target/target1.bmp')
tstore = t

def get_s_mean_std(s):

    s_meano, s_stdo = cv2.meanStdDev(s)
    s_mean = []
    s_std = []
    for item in s_meano:
        s_mean.append(round(item[0] , 2))

    for item in s_stdo:
        s_std.append(round(item[0] , 2))
    return s_mean ,s_std

print(get_s_mean_std(s))