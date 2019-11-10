from methods.simple.simple_method import *


class Bezier:
    @staticmethod
    def M():
        return Matrix([[-1, 3, -3, 1],
                       [3, -6, 3, 0],
                       [-3, 3, 0, 0],
                       [1, 0, 0, 0]])


class BezierParametric(Bezier, SimpleMethodParametric):
    def __init__(self, points):
        super(BezierParametric, self).__init__(points, self.M())


class BezierForwardDifferences(Bezier, SimpleMethodForwardDifferences):
    def __init__(self, points, n):
        super(BezierForwardDifferences, self).__init__(points, n)
