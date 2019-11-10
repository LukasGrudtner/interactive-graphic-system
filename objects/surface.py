from objects.wireframe import Wireframe
from methods.bicubic.bicubic_bezier import BicubicBezierParametric
from methods.bicubic.bicubic_bspline import *
from objects.point import Point
from objects.object import Object
import settings


class Surface:
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
        object = Object(self._name)

        wireframes = self.build()
        for wireframe in wireframes:
            self.connect_points(wireframe)
            object.add(wireframe)

        return object

    def connect_points(self, wireframe):
        points = wireframe.points()
        previous = points[0]

        for i in range(1, len(points)):
            current = points[i]
            wireframe.line(previous, current)
            previous = current

    def build(self):
        pass


class SurfaceBezier(Surface):
    def __init__(self, name="", points=None):
        super(SurfaceBezier, self).__init__(name, points)

    def build(self):
        wireframes = []

        i = 0
        while i+16 <= self.size():
            list = self._points[i:i+16]
            i += 16

            bezier = BicubicBezierParametric(list)
            curves = bezier.build()

            for curve in curves:
                wireframe = Wireframe()
                for point in curve:
                    wireframe.add_point(point.x(), point.y(), point.z())
                wireframes.append(wireframe)

        return wireframes


class SurfaceBSpline(Surface):
    def __init__(self, name="", points=None):
        super(SurfaceBSpline, self).__init__(name, points)

    def build(self):
        wireframes = []

        i = 0
        while i + 16 <= self.size():
            list = self._points[i:i+16]
            i += 1

            bspline = BicubicBSplineForwardDifferences(list, settings.FWD_DIFF_SURFACE_N, settings.FWD_DIFF_SURFACE_N)
            curves = bspline.build()

            wireframes = []
            for curve in curves[0]:
                wireframe = Wireframe()
                for point in curve:
                    wireframe.add_point(point.x(), point.y(), point.z())
                wireframes.append(wireframe)

            for curve in curves[1]:
                wireframe = Wireframe()
                for point in curve:
                    wireframe.add_point(point.x(), point.y(), point.z())
                wireframes.append(wireframe)

        return wireframes
