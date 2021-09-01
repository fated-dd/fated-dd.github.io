import numpy as np
import cv2
from sympy import Eq , symbols , solve
import statistics
import time



s = cv2.imread('static/source/source12.bmp')
sstore = s
t = cv2.imread('static/target/target1.bmp')
tstore = t


s_meano, s_stdo = cv2.meanStdDev(s)
s_mean = []
s_std = []
for item in s_meano:
    s_mean.append(round(item[0] , 2))

for item in s_stdo:
    s_std.append(round(item[0] , 2))

t_meano, t_stdo = cv2.meanStdDev(t)
t_mean = []
t_std = []

for item in t_meano:
    t_mean.append(round(item[0] , 2))

for item in t_stdo:
    t_std.append(round(item[0] , 2))

height , width , vac = s.shape
alphao = []
betao=[]

for n in range (0 , vac):
            x = symbols('x')
            equation1 = Eq( (x**2) * s_std[n] - t_std[n] , 0)
            result1 = solve(equation1)
            alphao.append(result1)
            y = symbols('y')
            equation2 = Eq(t_mean[n] - s_mean[n]*x , 0)
            result2 = solve(equation2)
            betao.append(result2)

alpha = []
beta = []

for i in range (0 , len(alphao)):
    alpha.append(round(alphao[i][1] , 3))

for i in range (0 , len(betao)):
    beta.append (round(betao[i][0] , 3))

print(alpha , beta)
time.sleep(0.5)
print('the size of the source image is: ' + str(height) + 'x' + str(width) + 'x' + str(vac))
time.sleep(1)

# print(alpha , beta)

print("Converting the picture...")
time.sleep(0.5)

times = 0

for i in range (0 , 10):
    for j in range (0 , 10):
        for n in range (0 , vac):
            pixel = s[i][j][n]
            print(pixel)
            print(alpha[n] , beta[n])
            # pixel = s[i , j , n]
            # print(pixel)
            newpixel = pixel*alpha[n] + beta[n]
            # if n == 1:
            #     pixel = pixel*alpha[n] + beta[n]
            # elif n == 2:
            #     pixel = pixel*alpha[n] + beta[n]
            # pixel = round(pixel)
            # if pixel < 0:
            #     pixel = 0
            # elif pixel > 255:
            #     pixel = 255
            sstore[i][j][n] = newpixel
            print(newpixel.round())
    times += 1
    print("Process: {}%".format(str((int((times/height)*1000)/10))) , end = '\r')

    
print('Convertion completed')
if s.all() == sstore.all():
    print(True)
else:
    print(False)

cv2.imwrite('result/result{}.bmp'.format(method) , sstore)
cv2.imshow('result' , sstore)
cv2.waitKey(0)
