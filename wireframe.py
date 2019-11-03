import transformations
from point import Point


class Wireframe:
    def __init__(self):
        self._points = []
        self._name = ""
        self._current_point_index = 0
        self._type = ""

    def set_name(self, _name):
        self._name = _name

    def get_point(self, index):
        if len(self._points) > index >= 0:
            return self._points[index]

    def points(self):
        return self._points

    def get_points(self):
        return self._points

    def set_points(self, _points):
        self._points = _points

    def get_name(self):
        return self._name

    def set_point(self, index, x, y, z):
        if 0 <= index < len(self._points):
            self._points[index] = Point(x, y, z)

    def remove_point(self, index):
        if 0 <= index < len(self._points):
            self._points.pop(index)

    def add_point(self, x, y, z):
        self._points.append(Point(x, y, z))
        self.update_type()
        return self

    def insert_point(self, point):
        self._points.append(point)
        self.update_type()

    def update_type(self):
        if self.n_points() == 1:
            self._type = "POINT"

        if self.n_points() > 1:
            self._type = "WIREFRAME"

    def object_type(self):
        return self._type

    def n_points(self):
        return len(self._points)

    def next_point(self):
        if self._current_point_index < len(self._points):
            current_point = self._points[self._current_point_index]
            self._current_point_index += 1
            return current_point

        return None

    def draw_points(self):
        return self._points

    def first_point(self):
        return self._points[0]

    def last_point(self):
        return self._points[-1]

    def center(self):
        cx = 0
        cy = 0
        cz = 0
        for point in self._points:
            cx += point.x()
            cy += point.y()
            cz += point.z()

        cx = cx / len(self._points)
        cy = cy / len(self._points)
        cz = cz / len(self._points)

        return Point(cx, cy, cz)

    def translate(self, dx, dy, dz):
        self.__transform__(transformations.translate(dx, dy, dz))

    def scale(self, sx, sy, sz):
        center = self.center()
        first_translate = transformations.translate(-center.x(), -center.y(), -center.z())
        scale = transformations.scale(sx, sy, sz)
        last_translate = transformations.translate(center.x(), center.y(), center.z())

        transformation = transformations.concat(transformations.concat(first_translate, scale), last_translate)
        self.__transform__(transformation)

    def rotate_z(self, degrees, center):
        self.__rotate__(center, transformations.rotate_z(degrees))

    def rotate_y(self, degrees, center):
        self.__rotate__(center, transformations.rotate_y(degrees))

    def rotate_x(self, degrees, center):
        self.__rotate__(center, transformations.rotate_x(degrees))

    def __rotate__(self, center, rotate):
        first_translate = transformations.translate(-center.x(), -center.y(), -center.z())
        last_translate = transformations.translate(center.x(), center.y(), center.z())

        transformation = transformations.concat(transformations.concat(first_translate, rotate), last_translate)
        self.__transform__(transformation)

    def __transform__(self, transformation):
        new_points = []
        for point in self._points:
            result = transformations.concat(point.to_array(), transformation)
            new_points.append(Point(result[0], result[1], result[2]))
        self.set_points(new_points)
