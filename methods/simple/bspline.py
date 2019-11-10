from methods.simple.simple_method import *


class BSpline:
    @staticmethod
    def M():
        return Matrix([[-1, 3, -3, 1],
                       [3, -6, 3, 0],
                       [-3, 3, 0, 0],
                       [1, 0, 0, 0]]) / 6


class BSplineParametric(BSpline, SimpleMethodParametric):
    def __init__(self, points):
        super(BSplineParametric, self).__init__(points, self.M())


class BSplineForwardDifferences(BSpline, SimpleMethodForwardDifferences):
    def __init__(self, points, n):
        super(BSplineForwardDifferences, self).__init__(points, self.M(), n)
