from point import Point
from bezier import Bezier
from hermite import Hermite
from wireframe import Wireframe


class Curve(Wireframe):
    def __init__(self):
        super(Curve, self).__init__()
        self.__name = ""

    def set_name(self, name):
        self.__name = name

    def add_point(self, x, y, z):
        self.points.append(Point(x, y, z))

    def get_name(self):
        return self.__name

    def points(self):
        return self.points


class CurveBezier(Curve):
    def __init__(self):
        super(CurveBezier, self).__init__()

    def get_points(self):
        return self.draw_points()

    def draw_points(self):
        counter = 0
        curve_points = []
        while counter + 4 <= len(self.points):
            bezier = Bezier(self.points[counter:counter + 4])
            curve_points += bezier.generate_points()
            counter += 3
        return curve_points


class CurveHermite(Curve):
    def __init__(self):
        super(CurveHermite, self).__init__()

    def get_points(self):
        return self.draw_points()

    def draw_points(self):
        counter = 0
        curve_points = []

        hermite = Hermite(self.points[0:4])
        curve_points += hermite.generate_points()
        counter += 4

        while counter < len(self.points):
            hermite = Hermite(
                [self.points[counter - 1], self.points[counter], self.points[counter - 2], self.points[counter+1]])
            curve_points += hermite.generate_points()
            counter += 2
        return curve_points
