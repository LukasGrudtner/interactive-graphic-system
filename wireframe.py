import transformations
from point import Point
from line import Line
import _thread


class Wireframe:
    def __init__(self):
        self._points = []
        self._lines = []
        self._transformation = None

    def add_point(self, x, y, z):
        self._points.append(Point(x, y, z, self.size()))
        return self._points[-1]

    def get_point(self, p):
        for point in self._points:
            if point == p:
                return point

    def get_point_by_id(self, id):
        for point in self._points:
            if point.id() == id:
                return point

    def points(self):
        return self._points

    def line(self, p1, p2):
        point1 = self.get_point(p1)
        point2 = self.get_point(p2)

        if point1 and point2:
            self._lines.append(Line(point1, point2))

    def pop(self, i):
        if i < self.size():
            self._lines.pop(i)

    def get(self, i):
        if i < self.size():
            return self._lines[i]

    def lines(self):
        return self._lines

    def size(self):
        return len(self._points)

    def center(self):
        cx, cy, cz = 0, 0, 0
        for point in self._points:
            cx += point.x()
            cy += point.y()
            cz += point.z()

        cx = cx / len(self._points)
        cy = cy / len(self._points)
        cz = cz / len(self._points)

        return Point(cx, cy, cz)

    def translate(self, dx, dy, dz):
        self.transform(transformations.translate(dx, dy, dz))

    def scale(self, sx, sy, sz):
        center = self.center()
        first_translate = transformations.translate(-center.x(), -center.y(), -center.z())
        scale = transformations.scale(sx, sy, sz)
        last_translate = transformations.translate(center.x(), center.y(), center.z())

        transformation = transformations.concat(transformations.concat(first_translate, scale), last_translate)
        self.transform(transformation)

    def rotate_z(self, degrees, center):
        self._rotate(center, transformations.rotate_z(degrees))

    def rotate_y(self, degrees, center):
        self._rotate(center, transformations.rotate_y(degrees))

    def rotate_x(self, degrees, center):
        self._rotate(center, transformations.rotate_x(degrees))

    def _rotate(self, center, rotate):
        first_translate = transformations.translate(-center.x(), -center.y(), -center.z())
        last_translate = transformations.translate(center.x(), center.y(), center.z())
        transformation = transformations.concat(transformations.concat(first_translate, rotate), last_translate)
        self.transform(transformation)

    def transform(self, transformation):
        return self.serial_transformation(transformation)

    def serial_transformation(self, transformation):
        for point in self._points:
            point.transform(transformation)
        return self

    def concurrent_transformation(self, trasformation):
        for point in self._points:
            _thread.start_new_thread(self._transform, (point, trasformation,))

    def _transform(self, point, transformation):
        point.transform(transformation)

    def str(self):
        str = ""
        for point in self._points:
            str += point.str()
            str += "\n"
        return str