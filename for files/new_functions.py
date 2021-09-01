import numpy as np
import cv2
from sympy import Eq , symbols , solve
import statistics
import time



s = cv2.imread('Program/source/source12.bmp')
sstore = s
t = cv2.imread('Program/target/target1.bmp')
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
        t_mean.append(round(statistics.mean(tlst[i]) , 2))
        t_std.append(round(np.std(tlst[i]) ,2))

    return t_mean , t_std


# print(s_mean , s_std , t_mean , t_std)


def normal_cal(s_mean , s_std , t_mean , t_std , method):
    
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

    time.sleep(0.5)
    print('the size of the source image is: ' + str(height) + 'x' + str(width) + 'x' + str(vac))
    time.sleep(0.5)


    for i in range (0 , len(alphao)):
        alpha.append(round(alphao[i][1] , 3))

    for i in range (0 , len(betao)):
        beta.append (round(betao[i][0] , 3))

    # print(alpha , beta)

    print("Converting the picture...")
    time.sleep(0.5)

    times = 0

    for i in range (0 , height):
        for j in range (0 , width):
            for n in range (0 , vac):
                pixel = s[i , j , n]
                # print(pixel)
                if n == 1:
                    pixel = pixel*alpha[n] + beta[n]
                elif n == 2:
                    pixel = pixel*alpha[n] + beta[n]
                # pixel = round(pixel)
                # if pixel < 0:
                #     pixel = 0
                # elif pixel > 255:
                #     pixel = 255
                sstore[i][j][n] = pixel
        times += 1
        print("Process: {}%".format(str((int((times/height)*1000)/10))) , end = '\r')

        
    print('Convertion completed')

    cv2.imwrite('Program/result/result{}.bmp'.format(method) , sstore)
    cv2.imshow('result' , sstore)
    cv2.waitKey(0)


def print_method(method):
    print(method)


def os():
    
    while True:

        method = input('Which method you want to use?:')

        if int(method) == 1:

            s_mean , s_std = get_normal_S_mean_std(s)
            t_mean , t_std = get_mormal_T_mean_std(t)
            normal_cal(s_mean , s_std , t_mean , t_std , method)
            break


        elif int(method) == 2:

            s_mean , s_std = get_normal_S_mean_std(s)
            t_mean , t_std = get_enhanced_T_mean_std(t)
            normal_cal(s_mean , s_std , t_mean , t_std , method)
            break
        

        elif int(method) == 4:
            print_method(method)
            break


        else:

            time.sleep(1)
            print('No such methods exists... Plz try again.')
            time.sleep(1)


os()
print('Goodbye!')