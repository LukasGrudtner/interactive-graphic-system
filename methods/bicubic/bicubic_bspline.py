from methods.simple.bspline import BSpline
from methods.bicubic.bicubic_method import *


class BicubicBSpline(BicubicMethod):
    def M(self):
        return BSpline.M()


class BicubicBSplineParametric(BicubicBSpline, BicubicMethodParametric):
    def __init__(self, points):
        super(BicubicBSpline, self).__init__(points, self.M())


class BicubicBSplineForwardDifferences(BicubicBSpline, BicubicMethodForwardDifferences):
    def __init__(self, points, ns, nt):
        super(BicubicBSplineForwardDifferences, self).__init__(points, self.M(), ns, nt)
