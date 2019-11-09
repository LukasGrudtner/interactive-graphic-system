import numpy as np
from sympy import *
from point import Point


class Bezier:
    def __init__(self, points):
        self._t = symbols('t')
        self._T = self.T()
        self._M = self.M()
        self._points = points

    def T(self):
        return Matrix([self._t ** 3, self._t ** 2, self._t, 1]).transpose()

    def M(self):
        return Matrix([[-1, 3, -3, 1],
                       [3, -6, 3, 0],
                       [-3, 3, 0, 0],
                       [1, 0, 0, 0]])

    def Gx(self):
        col = []
        i = 0
        for point in self._points:
            col.append(point.x())
            i += 1
        return Matrix([col]).transpose()

    def Gy(self):
        col = []
        i = 0
        for point in self._points:
            col.append(point.y())
            i += 1
        return Matrix([col]).transpose()

    def Gz(self):
        col = []
        i = 0
        for point in self._points:
            col.append(point.z())
            i += 1
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
            x = fx.subs(self._t, ti)
            y = fy.subs(self._t, ti)
            z = fz.subs(self._t, ti)
            points.append(Point(x, y, z))

        return points
