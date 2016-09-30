# coding:utf-8 #

from pylab import *
from scipy import signal as sg
from noise import sp_noise

import csv
import numpy as np
#####################################################################

class Pcnn_class():

    def PCNN(self, img_arr, iteration_num,
             Af = 0.60, Al = 1.0, Atop = 0.80,
             Vf = 0.2, Vl = 0.2, Vtop = 2000.0,
             Beta = 0.1):
        # 获得矩阵的维度

        x_len, y_len = img_arr.shape

        # E = np.eye(x_len, dtype="float64")

        # 定义神经元矩阵，建立n=0时的F、L矩阵（都为0矩阵）

        W = np.array([[0.7070, 1, 0.7070], [1, 0, 1], [0.7070, 1, 0.7070]])
        M = np.array([[0.7070, 1, 0.7070], [1, 0, 1], [0.7070, 1, 0.7070]])
        Y = np.zeros_like(img_arr, dtype="float64")
        F = np.zeros_like(img_arr, dtype="float64")
        L = np.zeros_like(img_arr, dtype="float64")
        top = np.zeros_like(img_arr, dtype="float64") + 200.0

        # 定义点火过程
        temp = img_arr
        for i in range(0, iteration_num):

            K = sg.convolve2d(Y, M, mode="same")
            # print "第 %s 次迭代，K矩阵：" % i, "\n", K
            # raw_input("=================================")
            F = exp(-Af) * F + Vf * K
            L = exp(-Al) * L + Vl * K
            # print "第 %s 次迭代，L矩阵：" % i, "\n", L
            # raw_input("=================================")
            U = F * (1 + Beta * L)
            top = exp(-Atop) * top + Vtop * Y
            # print top
            # raw_input("top====================================")
            for x_axis in range(0, x_len):
                for y_axis in range(0, y_len):

                    if (U[x_axis, y_axis] > top[x_axis, y_axis]):
                        Y[x_axis, y_axis] = 1.0

                    else:
                        Y[x_axis, y_axis] = 0.0

            print len(Y[Y==1])
            print "第 %s 次迭代完成。\n" % i

# raw_input("=============================================")
#         print U
        return U

#####################################################################

# 获得图像矩阵

if __name__ == "__main__":

    # img = imread('/home/qiujiayu/图片/10_lena.jpg')
    csvfile = file('/home/qiujiayu/文档/3_lena.csv', 'rb')
    img = []
    for line in csvfile:
        img.append(line.split(','))

    img = [[float(y) for y in x]for x in img]
    img = np.array(img)

    noise_img = sp_noise(img, 0.05)
    # raw_input("================================")
    img_matlab = imread('/home/qiujiayu/图片/untitled.jpg')

    # 将图像矩阵归一化

    # img_normalized = np.array([[[float(rgb/255.0) for rgb in y_axis] for y_axis in x_axis] for x_axis in img])
    # img_nor = np.array([[float(axis/255.0) for axis in line]for line in img])

    p=Pcnn_class()
    img_out = p.PCNN(img_arr=img, iteration_num=30)
    # img_out = img_out * 255.0

    # print img_out
    # raw_input("===========================================")
    print "done!"

    gray()
    imshow(noise_img)
    show()

