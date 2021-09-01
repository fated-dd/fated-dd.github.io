import numpy as np
import cv2
from sympy import Eq , symbols , solve
import statistics
import time




def process(s, t):

    s = cv2.imread(s)
    t = cv2.imread(t)

    s = cv2.cvtColor(s,cv2.COLOR_BGR2LAB)
    sstore = cv2.cvtColor(s,cv2.COLOR_BGR2LAB)

    t = cv2.cvtColor(t,cv2.COLOR_BGR2LAB)
    tstore = cv2.cvtColor(t,cv2.COLOR_BGR2LAB)


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


    def normal_cal(s_mean , s_std , t_mean , t_std):
        
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
        print('the size of the source image is: ' + str(height) + 'x' + str(width) + 'x' + str(vac))

        # print(alpha , beta)

        print("Converting the picture...")

        times = 0

        for i in range (0 , height):
            for j in range (0 , width):
                for k in range (0 , vac):
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

        cv2.imwrite('result/result.bmp', sstore)
        cv2.imshow('result' , sstore)
        cv2.waitKey(0)
        return 'result/result.bmp'


    s_mean , s_std = get_normal_S_mean_std(s)
    t_mean , t_std = get_mormal_T_mean_std(t)
    result = normal_cal(s_mean , s_std , t_mean , t_std)
    return result




def main():
    print("execute only if called directly")

if __name__ == "__main__":
    main()