from point import Point
from bezier import Bezier
from hermite import Hermite
from bspline import BSpline
from wireframe import Wireframe
import settings


class Curve(Wireframe):
    def __init__(self):
        super(Curve, self).__init__()

    def get_points(self):
        return self.draw_points()

    def to_wireframe(self):
        wireframe = Wireframe()
        wireframe.set_name(self.get_name())
        wireframe.set_points(self.draw_points())
        return wireframe


class CurveBezier(Curve):
    def __init__(self):
        super(CurveBezier, self).__init__()

    def draw_points(self):
        counter = 0
        curve_points = []
        while counter + 4 <= self.n_points():
            bezier = Bezier(self.points()[counter:counter + 4])
            curve_points += bezier.generate_points()
            counter += 3
        return curve_points


class CurveHermite(Curve):
    def __init__(self):
        super(CurveHermite, self).__init__()

    def draw_points(self):
        counter = 0
        curve_points = []

        hermite = Hermite(self.points()[0:4])
        curve_points += hermite.generate_points()
        counter += 4

        while counter < self.n_points():
            hermite = Hermite(
                [self.points()[counter - 1], self.points()[counter], self.points()[counter - 2], self.points()[counter + 1]])
            curve_points += hermite.generate_points()
            counter += 2
        return curve_points


class CurveBSpline(Curve):
    def __init__(self):
        super(CurveBSpline, self).__init__()

    def get_points(self):
        return self.draw_points()

    def draw_points(self):
        counter = 0
        curve_points = []

        while counter + 4 <= self.n_points():
            bspline = BSpline(self.points()[counter:counter + 4])
            curve_points += bspline.generate_points(settings.FWD_DIFF_STEPS)
            counter += 1

        return curve_points
