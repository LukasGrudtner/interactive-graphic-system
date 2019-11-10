from sympy import Matrix
from objects.point import Point
import numpy as np
from methods import parametric, forward_differences


class BicubicMethod:
    def __init__(self, points, M):
        self._points = points
        self._M = M

    def Gx(self):
        def builder(i, j):
            return self._points[i * 4 + j].x()

        return Matrix(4, 4, builder)

    def Gy(self):
        def builder(i, j):
            return self._points[i * 4 + j].y()

        return Matrix(4, 4, builder)

    def Gz(self):
        def builder(i, j):
            return self._points[i * 4 + j].z()

        return Matrix(4, 4, builder)


class BicubicMethodParametric(BicubicMethod):
    def __init__(self, points, M):
        super(BicubicMethodParametric, self).__init__(points, M)

    def fx(self):
        fx = parametric.S() * self._M * self.Gx() * self._M.transpose() * parametric.T().transpose()
        return fx[0]

    def fy(self):
        fy = parametric.S() * self._M * self.Gy() * self._M.transpose() * parametric.T().transpose()
        return fy[0]

    def fz(self):
        fz = parametric.S() * self._M * self.Gz() * self._M.transpose() * parametric.T().transpose()
        return fz[0]

    def build(self):
        fx, fy, fz = self.fx(), self.fy(), self.fz()
        ss = np.arange(0, 1, 0.01)
        ts = np.arange(0, 1, 0.1)

        curves = []
        for si in ss:
            points = []
            for ti in ts:
                x = fx.subs([(parametric.t(), ti), (parametric.s(), si)])
                y = fy.subs([(parametric.t(), ti), (parametric.s(), si)])
                z = fz.subs([(parametric.t(), ti), (parametric.s(), si)])
                points.append(Point(x, y, z))
            curves.append(points)

        return curves


class BicubicMethodForwardDifferences(BicubicMethod):
    def __init__(self, points, M, ns, nt):
        super(BicubicMethodForwardDifferences, self).__init__(points, M)
        self._ns = ns
        self._nt = nt

    def generate_forward_differences_matrix(self, G, Es, Et):
        C = self._M * G * self._M.transpose()
        return Es * C * Et

    def draw_curves_s(self, n, Gx, Gy, Gz, Es, Et):
        DDx = self.generate_forward_differences_matrix(Gx, Es, Et)
        DDy = self.generate_forward_differences_matrix(Gy, Es, Et)
        DDz = self.generate_forward_differences_matrix(Gz, Es, Et)

        curves = []
        for i in range(n):
            points = forward_differences.draw_curve(n, DDx, DDy, DDz)
            curves.append(points)

            DDx = forward_differences.update_matrix(DDx)
            DDy = forward_differences.update_matrix(DDy)
            DDz = forward_differences.update_matrix(DDz)

        return curves

    def draw_curves_t(self, n, Gx, Gy, Gz, Es, Et):
        DDx = self.generate_forward_differences_matrix(Gx, Es, Et).transpose()
        DDy = self.generate_forward_differences_matrix(Gy, Es, Et).transpose()
        DDz = self.generate_forward_differences_matrix(Gz, Es, Et).transpose()

        curves = []
        for i in range(n):
            points = forward_differences.draw_curve(n, DDx, DDy, DDz)
            curves.append(points)

            DDx = forward_differences.update_matrix(DDx)
            DDy = forward_differences.update_matrix(DDy)
            DDz = forward_differences.update_matrix(DDz)

        return curves

    def build(self):
        delta_s = 1 / (self._ns - 1)
        delta_t = 1 / (self._nt - 1)

        Es = forward_differences.E(delta_s)
        Et = forward_differences.E(delta_t).transpose()

        Gx, Gy, Gz = self.Gx(), self.Gy(), self.Gz()

        curves_s = self.draw_curves_s(self._nt, Gx, Gy, Gz, Es, Et)
        curves_t = self.draw_curves_t(self._ns, Gx, Gy, Gz, Es, Et)

        return curves_t, curves_s
