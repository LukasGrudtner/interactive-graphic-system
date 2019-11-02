import numpy as np
from sympy import *
from point import Point


class BSpline:
    def __init__(self, points):
        self._points = points

    @staticmethod
    def _generate_E(delta):
        return Matrix([[0, 0, 0, 1],
                       [delta ** 3, delta ** 2, delta, 0],
                       [6 * delta ** 3, 2 * delta ** 2, 0, 0],
                       [6 * delta ** 3, 0, 0, 0]])

    @staticmethod
    def _M():
        return Matrix([[-1, 3, -3, 1],
                       [3, -6, 3, 0],
                       [-3, 0, 3, 0],
                       [1, 4, 1, 0]]) / 6

    def _Gx(self):
        Gx = []
        for point in self._points:
            Gx.append(point.x())
        return Matrix([Gx]).transpose()

    def _Gy(self):
        Gy = []
        for point in self._points:
            Gy.append(point.y())
        return Matrix([Gy]).transpose()

    def _generate_forward_differences_matrix(self, G, E):
        C = self._M() * G
        return E * C

    @staticmethod
    def _draw_curve_forward_differences(n, DDx, DDy):
        oldx = np.array(DDx).item(0)
        Dx = np.array(DDx).item(1)
        D2x = np.array(DDx).item(2)
        D3x = np.array(DDx).item(3)

        oldy = np.array(DDy).item(0)
        Dy = np.array(DDy).item(1)
        D2y = np.array(DDy).item(2)
        D3y = np.array(DDy).item(3)

        points = []

        for i in range(n):
            x = oldx + Dx
            Dx = Dx + D2x
            D2x = D2x + D3x

            y = oldy + Dy
            Dy = Dy + D2y
            D2y = D2y + D3y

            points.append(Point(oldx, oldy, 1))

            oldx = x
            oldy = y

        return points

    def generate_points(self, n):
        delta = 1 / (n - 1)
        E = self._generate_E(delta)
        Gx = self._Gx()
        Gy = self._Gy()
        DDx = self._generate_forward_differences_matrix(Gx, E)
        DDy = self._generate_forward_differences_matrix(Gy, E)

        return self._draw_curve_forward_differences(n, DDx, DDy)
