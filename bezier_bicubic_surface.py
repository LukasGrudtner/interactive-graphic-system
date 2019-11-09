import numpy as np
from sympy import *
from point import Point
from bezier import Bezier


class BezierBicubicSurface(Bezier):
    def __init__(self, points):
        self._s = symbols('s')
        self._S = self.S()
        self._M = self.M()
        self._t = symbols('t')
        self._T = self.T()
        self._points = points
        self._fx = self.fx()
        self._fy = self.fy()
        self._fz = self.fz()

    def S(self):
        return Matrix([self._s ** 3, self._s ** 2, self._s, 1]).transpose()

    def _Gx(self):
        Gx = zeros(4, 4)
        i = 0
        row = []
        column = 0

        for point in self._points:
            if column == 4:
                Gx.row_del(i)
                Gx = Gx.row_insert(i, Matrix([row]))
                i += 1
                row = []
                column = 0
            row.append(point.x())
            column += 1

        Gx.row_del(i)
        return Gx.row_insert(i, Matrix([row]))

    def _Gy(self):
        Gy = zeros(4, 4)
        i = 0
        row = []
        column = 0

        for point in self._points:
            if column == 4:
                Gy.row_del(i)
                Gy = Gy.row_insert(i, Matrix([row]))
                i += 1
                row = []
                column = 0
            row.append(point.y())
            column += 1

        Gy.row_del(i)
        return Gy.row_insert(i, Matrix([row]))

    def _Gz(self):
        Gz = zeros(4, 4)
        i = 0
        row = []
        column = 0

        for point in self._points:
            if column == 4:
                Gz.row_del(i)
                Gz = Gz.row_insert(i, Matrix([row]))
                i += 1
                row = []
                column = 0
            row.append(point.z())
            column += 1

        Gz.row_del(i)
        return Gz.row_insert(i, Matrix([row]))

    def fx(self):
        fx = self._S * self._M * self._Gx() * self._M.transpose() * self._T.transpose()
        return fx[0]

    def fy(self):
        fy = self._S * self._M * self._Gy() * self._M.transpose() * self._T.transpose()
        return fy[0]

    def fz(self):
        fz = self._S * self._M * self._Gz() * self._M.transpose() * self._T.transpose()
        return fz[0]

    def build(self):
        ss = np.arange(0, 1, 0.01)
        ts = np.arange(0, 1, 0.1)

        curves = []
        for si in ss:
            points = []
            for ti in ts:
                x = self._fx.subs([(self._t, ti), (self._s, si)])
                y = self._fy.subs([(self._t, ti), (self._s, si)])
                z = self._fz.subs([(self._t, ti), (self._s, si)])
                points.append(Point(x, y, z))
            curves.append(points)

        return curves
