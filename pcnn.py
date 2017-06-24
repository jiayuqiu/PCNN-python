# coding:utf-8

from pylab import *
from scipy import signal as sg
from noise import sp_noise

############################################################################################
class pcnn(object):
    """pcnn类"""

    #--------------------------------------------------------------------------------------
    def __init__(self, iterationNum = 10):
        """初始化pcnn参数"""
        # 迭代次数
        self.iterationNum = iterationNum

        # 馈送输入的时间衰减常数
        self.Af = 0.60

        # 链接输入的时间衰减常数
        self.Al = 1.00

        # 动态门限的时间衰减常数
        self.Atop = 0.80

        # 馈送输入的放大系数
        self.Vf = 0.20

        # 链接输入的放大系数
        self.Vl = 0.20

        # 动态门限的放大系数
        self.Vtop = 2000.

        # 内部链接因子
        self.beta = 0.1

        # 动态门限初始值
        self.topInitValue = 200.

        # 神经元联系矩阵
        self.M = np.array([[0.7070, 1, 0.7070], [1, 0, 1], [0.7070, 1, 0.7070]])

    #---------------------------------------------------------------------------------------
    def initArr(self, imgArr):
        """初始化神经元矩阵"""
        # 脉冲矩阵
        Y = np.zeros_like(imgArr, dtype="float64")

        # 反馈输入矩阵
        F = np.zeros_like(imgArr, dtype="float64")

        # 耦合链接
        L = np.zeros_like(imgArr, dtype="float64")

        # 动态门限
        top = np.zeros_like(imgArr, dtype="float64") + self.topInitValue

        return [Y, F, L, top]

    #---------------------------------------------------------------------------------------
    def fire(self, pmtArr):
        """pcnn点火过程"""

        x_len, y_len = pmtArr[0].shape
        for i in range(0, self.iterationNum):
            K = sg.convolve2d(pmtArr[0], self.M, mode="same")
            F = exp(-self.Af) * pmtArr[1] + self.Vf * K
            L = exp(-self.Al) * pmtArr[2] + self.Vl * K
            U = F * (1 + self.beta * L)
            top = exp(-self.Atop) * pmtArr[3] + self.Vtop * pmtArr[3]
            for x_axis in range(0, x_len):
                for y_axis in range(0, y_len):

                    if (U[x_axis, y_axis] > top[x_axis, y_axis]):
                        pmtArr[0][x_axis, y_axis] = 1.0

                    else:
                        pmtArr[0][x_axis, y_axis] = 0.0

            print "第 %s 次迭代完成。\n" % i
        return U

    #---------------------------------------------------------------------------------------
    def pcnnMain(self, imgArr):
        """pcnn主函数
        
        输入：imgArr - 图像矩阵
             iterationNum - 迭代次数，默认10次
        """
        # 初始化神经元矩阵，并建立n=0时，F,L矩阵
        pass

if __name__ == "__main__":
    print("hello world!")
