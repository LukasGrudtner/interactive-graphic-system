from point import Point
from bezier import Bezier
from hermite import Hermite
from bspline import BSpline
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

    def connect_points(self, points, wireframe):
        previous = points[0]
        wireframe.add_point(previous.x(), previous.y(), previous.z())

        for i in range(1, len(points)):
            current = points[i]
            current = wireframe.add_point(current.x(), current.y(), current.z())
            wireframe.line(previous, current)
            previous = current

    def build(self):
        pass


class CurveBezier(Curve):
    def __init__(self, name="", points=None):
        super(CurveBezier, self).__init__(name, points)

    def build(self):
        counter, points = 0, []
        while counter + 4 <= self.size():
            bezier = Bezier(self._points[counter:counter + 4])
            points += bezier.build()
            counter += 3
        return points


class CurveHermite(Curve):
    def __init__(self, name="", points=None):
        super(CurveHermite, self).__init__(name, points)

    def build(self):
        counter, points = 0, []

        hermite = Hermite(self._points[0:4])
        points += hermite.build()
        counter += 4

        while counter < self.size():
            hermite = Hermite(
                [self._points[counter - 1], self._points[counter], self._points[counter - 2],
                 self._points[counter + 1]])
            points += hermite.build()
            counter += 2
        return points


class CurveBSpline(Curve):
    def __init__(self, name="", points=None):
        super(CurveBSpline, self).__init__(name, points)

    def build(self):
        counter, points = 0, []
        while counter + 4 <= self.size():
            bspline = BSpline(self._points[counter:counter + 4])
            points += bspline.build(settings.FWD_DIFF_STEPS)
            counter += 1
        return points
