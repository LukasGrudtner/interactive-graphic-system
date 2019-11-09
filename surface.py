from wireframe import Wireframe
from bezier_bicubic_surface import BezierBicubicSurface
from point import Point
from object import Object


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
        bezier = BezierBicubicSurface(self._points)
        curves = bezier.build()
        wireframes = []

        for curve in curves:
            wireframe = Wireframe()
            for point in curve:
                wireframe.add_point(point.x(), point.y(), point.z())
            wireframes.append(wireframe)

        return wireframes
