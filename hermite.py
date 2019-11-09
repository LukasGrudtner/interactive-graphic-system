import numpy as np
from sympy import *
from point import Point


class Hermite:
    def __init__(self, points):
        self.__t = symbols('t')
        self.__T = self.T()
        self.__M = self.M()
        self.__points = points

    def T(self):
        return Matrix([self.__t ** 3, self.__t ** 2, self.__t, 1]).transpose()

    def M(self):
        return Matrix([[2, -2, 1, 1],
                       [-3, 3, -2, -1],
                       [0, 0, 1, 0],
                       [1, 0, 0, 0]])

    def Gx(self):
        col = [self.__points[0].x(), self.__points[3].x(), self.__points[1].x(), self.__points[2].x()]
        return Matrix([col]).transpose()

    def Gy(self):
        col = [self.__points[0].y(), self.__points[3].y(), self.__points[1].y(), self.__points[2].y()]
        return Matrix([col]).transpose()

    def Gz(self):
        col = [self.__points[0].z(), self.__points[3].z(), self.__points[1].z(), self.__points[2].z()]
        return Matrix([col]).transpose()

    def fx(self):
        fx = self.T() * self.M() * self.Gx()
        return fx[0]

    def fy(self):
        fy = self.T() * self.M() * self.Gy()
        return fy[0]

    def fz(self):
        fz = self.T() * self.M() * self.Gz()
        return fz[0]

    def build(self):
        fx = self.fx()
        fy = self.fy()
        fz = self.fz()

        ts = np.arange(0, 1, 0.01)

        points = []
        for ti in ts:
            x = fx.subs(self.__t, ti)
            y = fy.subs(self.__t, ti)
            z = fz.subs(self.__t, ti)
            points.append(Point(x, y, z))

        return points
