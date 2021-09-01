from math import pi
import numpy as np
import cv2
from sympy import Eq , symbols , solve
import statistics
import time
import os



s = cv2.imread('static/source/sourcesky.bmp')
sstore = s
t = cv2.imread('static/target/target12.bmp')
tstore = t



def get_normal_S_mean_std(s):

    s_meano, s_stdo = cv2.meanStdDev(s)
    s_mean = []
    s_std = []
    for item in s_meano:
        s_mean.append(round(item[0] , 2))

    for item in s_stdo:
        s_std.append(round(item[0] , 2))
    return s_mean , s_std


def get_mormal_T_mean_std(t):

    t_meano, t_stdo = cv2.meanStdDev(t)
    t_mean = []
    t_std = []

    for item in t_meano:
        t_mean.append(round(item[0] , 2))

    for item in t_stdo:
        t_std.append(round(item[0] , 2))
    return t_mean , t_std


def get_enhanced_T_mean_std(t):
    s_mean , s_std = get_normal_S_mean_std(s)
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

    print('The percentage of pixels picked in target is ' + str(round(len(tlst[0])/(theight*twidth)*100 , 2)) + '%')
    time.sleep(0.5)

    for i in range (len(tlst)):
        t_mean.append(round(((statistics.mean(tlst[i])) + s_mean[i])/2 , 2))
        t_std.append(round(((np.std(tlst[i])) + s_std[i])/2 ,2))

    return t_mean , t_std

# print(s_mean , s_std , t_mean , t_std)

def get_mean_and_std(x):
	x_mean, x_std = cv2.meanStdDev(x)
	x_mean = np.hstack(np.around(x_mean,2))
	x_std = np.hstack(np.around(x_std,2))
	return x_mean, x_std


def advanced_cal(s , t):
    count = 0
    print("Converting picture...")
    s = cv2.cvtColor(s,cv2.COLOR_BGR2LAB)
    t = cv2.cvtColor(t,cv2.COLOR_BGR2LAB)
    s_mean, s_std = get_mean_and_std(s)
    t_mean, t_std = get_mean_and_std(t)
    height, width, vac = s.shape

    for i in range(0 , height):
        for j in range(0 , width):
            for n in range(0 , vac):
                x = s[i,j,n]
                2
                x = t_mean[n] + ((t_std[n] / s_std[n]) * (x - s_mean[n]))
				# round or +0.5
                x = round(x)
				# boundary check
                x = 0 if x<0 else x
                x = 255 if x>255 else x

                s[i,j,n] = x
        count += 1
        print("Process: {}%".format(str((int((count/height)*1000)/10))) , end = '\r')

    s = cv2.cvtColor(s,cv2.COLOR_LAB2BGR)
    cv2.imwrite('result.bmp' , s)
    cv2.imshow('result.bmp' , s)
    cv2.waitKey(0)


def normal_cal(s , t , method):

    print("Converting picture...")
    if method == '1':
        s_mean, s_std = get_normal_S_mean_std(s)
        t_mean, t_std = get_mormal_T_mean_std(t)
    elif method == '2':
        s_mean, s_std = get_normal_S_mean_std(s)
        t_mean, t_std = get_enhanced_T_mean_std(t)
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

    for i in range (0 , height):
        for j in range (0 , width):
            for n in range (0 , vac):
                    pixel = s[i , j , n]
                    pixel = pixel*alpha[n] + beta[n]
                    # pixel = ((pixel-s_mean[n])*(t_std[n]/s_std[n]))+t_mean[n]
                    # pixel = round(pixel)
                    # if pixel < 0:
                    #     pixel = 0
                    # elif pixel > 255:
                    #     pixel = 255
                    
                    pixel = round(pixel)
                    pixel = 0 if pixel < 0 else pixel
                    pixel = 255 if pixel > 255 else pixel
                    sstore[i][j][n] = pixel
                    # x = s[i,j,k]
                    # x = ((x-s_mean[k])*(t_std[k]/s_std[k]))+t_mean[k]
                    # # round or +0.5
                    # x = round(x)
                    # # boundary check
                    # x = 0 if x<0 else x
                    # x = 255 if x>255 else x
                    # s[i,j,k] = x
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


def print_method(method):
    print(method)


def os():

    print('''Welcome welcome!

    Method 1: normal transferring
    Method 2: enhanced the contrastive part in the target
    Method 3: CIELAB method for transferring
    Key in 'Quit' to quit the program''')
    
    time.sleep(1)
    print('''Now key in your option!
    ''')
    time.sleep(1)
    
    while True:
        
        method = input('Which method you want to use?:')

        if int(method) == 1:
            normal_cal(s , t , method)
            break


        elif int(method) == 2:
            normal_cal(s , t , method)
            break

        elif int(method) == 3:
            advanced_cal(s , t)
            break
        

        elif int(method) == 4:
            print_method(method)
            break


        elif method == 'Quit' or 'quit':
            break


        else:

            time.sleep(1)
            print('No such methods exists... Plz try again.')
            time.sleep(1)
        

os()
print('Goodbye!')
time.sleep(1)
