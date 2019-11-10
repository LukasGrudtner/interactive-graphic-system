from point import Point
from methods.simple.bezier import BezierParametric, BezierForwardDifferences
from methods.simple.hermite import HermiteParametric, HermiteForwardDifferences
from methods.simple.bspline import BSplineParametric, BSplineForwardDifferences
from wireframe import Wireframe
from object import Object
import settings


class Curve:
    def __init__(self, name="", points=None):
        self._name = name
        if points is None:
            points = []
        self._points = points

    def add_point(self, x, y, z):
        self._points.append(Point(x, y, z))

    def size(self):
        return len(self._points)

    def to_object(self):
        wireframe = Wireframe()
        points = self.build()
        self.connect_points(points, wireframe)

        object = Object(self._name)
        object.add(wireframe)

        return object

    @staticmethod
    def connect_points(points, wireframe):
        previous = points[0]
        wireframe.add_point(previous.x(), previous.y(), previous.z())

        for i in range(1, len(points)):
            current = points[i]
            current = wireframe.add_point(current.x(), current.y(), current.z())
            wireframe.line(previous, current)
            previous = current


class CurveBezierParametric(Curve):
    def __init__(self, name="", points=None):
        super(CurveBezierParametric, self).__init__(name, points)

    def build(self):
        counter, points = 0, []
        while counter + 4 <= self.size():
            bezier = BezierParametric(self._points[counter:counter + 4])
            points += bezier.build()
            counter += 3
        return points


class CurveBezierForwardDifferences(Curve):
    def __init__(self, name="", points=None):
        super(CurveBezierForwardDifferences, self).__init__(name, points)

    def build(self):
        counter, points = 0, []
        while counter + 4 <= self.size():
            bezier = BezierForwardDifferences(self._points[counter:counter + 4], settings.FWD_DIFF_STEPS)
            points += bezier.build()
            counter += 3
        return points


class CurveHermiteParametric(Curve):
    def __init__(self, name="", points=None):
        super(CurveHermiteParametric, self).__init__(name, points)

    def build(self):
        counter, points = 0, []

        hermite = HermiteParametric(self._points[0:4])
        points += hermite.build()
        counter += 4

        while counter < self.size():
            hermite = HermiteParametric(
                [self._points[counter - 1], self._points[counter], self._points[counter - 2],
                 self._points[counter + 1]])
            points += hermite.build()
            counter += 2
        return points


class CurveHermiteForwardDifferences(Curve):
    def __init__(self, name="", points=None):
        super(CurveHermiteForwardDifferences, self).__init__(name, points)

    def build(self):
        counter, points = 0, []

        hermite = HermiteParametric(self._points[0:4])
        points += hermite.build()
        counter += 4

        while counter < self.size():
            hermite = HermiteForwardDifferences(
                [self._points[counter - 1], self._points[counter], self._points[counter - 2],
                 self._points[counter + 1]], settings.FWD_DIFF_STEPS)
            points += hermite.build()
            counter += 2
        return points


class CurveBSplineParametric(Curve):
    def __init__(self, name="", points=None):
        super(CurveBSplineParametric, self).__init__(name, points)

    def build(self):
        counter, points = 0, []
        while counter + 4 <= self.size():
            bspline = BSplineParametric(self._points[counter:counter + 4], settings.FWD_DIFF_STEPS)
            points += bspline.build
            counter += 1
        return points


class CurveBSplineForwardDifferences(Curve):
    def __init__(self, name="", points=None):
        super(CurveBSplineForwardDifferences, self).__init__(name, points)

    def build(self):
        counter, points = 0, []
        while counter + 4 <= self.size():
            bspline = BSplineForwardDifferences(self._points[counter:counter + 4], settings.FWD_DIFF_STEPS)
            points += bspline.build()
            counter += 1
        return points
