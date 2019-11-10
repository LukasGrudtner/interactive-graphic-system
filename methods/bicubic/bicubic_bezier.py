from methods.simple.bezier import Bezier
from methods.bicubic.bicubic_method import *


class BicubicBezier(BicubicMethod):
    def M(self):
        return Bezier.M()


class BicubicBezierParametric(BicubicBezier, BicubicMethodParametric):
    def __init__(self, points):
        super(BicubicBezierParametric, self).__init__(points, self.M())


class BicubicBezierForwardDifferences(BicubicBezier, BicubicMethodForwardDifferences):
    def __init__(self, points, ns, nt):
        super(BicubicBezierForwardDifferences, self).__init__(points, self.M(), ns, nt)
