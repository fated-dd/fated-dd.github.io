import numpy as np
import cv2
from sympy import Eq , symbols , solve
import statistics

s = cv2.imread('Program/source/source12.bmp')
sstore = s
t = cv2.imread('Program/target/target1.bmp')
tstore = t


t_mean = []
t_std = []

theight, twidth, tvac = t.shape
tlst = [[] , [] ,[]]
for i in range (0 , theight):
    for o in range (0 , twidth):
        if max(tstore[i][o]) - min(tstore[i][o]) < 50:
            continue
        else:
            for p in range (0 , tvac):
                tlst[p].append(tstore[i][o][p])
print(theight*twidth)
print(len(tlst[0]))       
# print(statistics.mean(tlst[0]))

for i in range (len(tlst)):
    t_mean.append(round(statistics.mean(tlst[i]) , 2))
    t_std.append(round(np.std(tlst[i]) ,2))



