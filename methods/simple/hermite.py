from methods.simple.simple_method import *


class Hermite:

    @staticmethod
    def M():
        return Matrix([[2, -2, 1, 1],
                       [-3, 3, -2, -1],
                       [0, 0, 1, 0],
                       [1, 0, 0, 0]])

    def swap(self, points):
        points[1], points[2], points[3] = points[3], points[1], points[2]
        return points


class HermiteParametric(Hermite, SimpleMethodParametric):
    def __init__(self, points):
        super(HermiteParametric, self).__init__(self.swap(points), self.M())


class HermiteForwardDifferences(Hermite, SimpleMethodForwardDifferences):
    def __init__(self, points, n):
        super(HermiteForwardDifferences, self).__init__(self.swap(points), self.M(), n)
