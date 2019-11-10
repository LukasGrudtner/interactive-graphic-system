from sympy import Matrix
from methods import parametric, forward_differences
from objects.point import Point
import numpy as np


class SimpleMethod:
    def __init__(self, points, M):
        self._points = points
        self._M = M

    def Gx(self):
        return Matrix(len(self._points), 1, lambda i, j: self._points[i].x())

    def Gy(self):
        return Matrix(len(self._points), 1, lambda i, j: self._points[i].y())

    def Gz(self):
        return Matrix(len(self._points), 1, lambda i, j: self._points[i].z())


class SimpleMethodParametric(SimpleMethod):
    def __init__(self, points, M):
        super(SimpleMethodParametric, self).__init__(points, M)

    def fx(self):
        fx = parametric.T() * self._M * self.Gx()
        return fx[0]

    def fy(self):
        fy = parametric.T() * self._M * self.Gy()
        return fy[0]

    def fz(self):
        fz = parametric.T() * self._M * self.Gz()
        return fz[0]

    def build(self):
        fx, fy, fz = self.fx(), self.fy(), self.fz()
        ts = np.arange(0, 1, 0.01)

        points = []
        for ti in ts:
            x = fx.subs(parametric.t(), ti)
            y = fy.subs(parametric.t(), ti)
            z = fz.subs(parametric.t(), ti)
            points.append(Point(x, y, z))

        return points


class SimpleMethodForwardDifferences(SimpleMethod):
    def __init__(self, points, M, n):
        super(SimpleMethodForwardDifferences, self).__init__(points, M)
        self._n = n

    def generate_forward_differences_matrix(self, G, E):
        C = self._M * G
        return E * C

    def build(self):
        delta = 1 / (self._n - 1)
        E = forward_differences.E(delta)
        Gx, Gy, Gz = self.Gx(), self.Gy(), self.Gz()

        DDx = self.generate_forward_differences_matrix(Gx, E)
        DDy = self.generate_forward_differences_matrix(Gy, E)
        DDz = self.generate_forward_differences_matrix(Gz, E)

        return forward_differences.draw_curve(self._n, DDx, DDy, DDz)
