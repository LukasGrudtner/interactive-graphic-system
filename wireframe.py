import transformations
from point import Point

class Wireframe:
    def __init__(self):
        self.points = []
        self.name = ""
        self.current_point_index = 0
        self.type = ""

    def set_name(self, name):
        self.name = name

    def get_point(self, index):
        if len(self.points) > index >= 0:
            return self.points[index]

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def get_name(self):
        return self.name

    def set_point(self, index, x, y, z):
        if 0 <= index < len(self.points):
            self.points[index] = Point(x, y, z)

    def remove_point(self, index):
        if 0 <= index < len(self.points):
            self.points.pop(index)

    def add_point(self, x, y, z):
        self.points.append(Point(x, y, z))
        self.update_type()
        return self

    def update_type(self):
        if self.n_points() == 1:
            self.type = "POINT"

        if self.n_points() > 1:
            self.type = "WIREFRAME"

    def object_type(self):
        return self.type

    def n_points(self):
        return len(self.points)

    def next_point(self):
        if self.current_point_index < len(self.points):
            current_point = self.points[self.current_point_index]
            self.current_point_index += 1
            return current_point

        return None

    def draw_points(self):
        return self.points + [self.points[0]]

    def first_point(self):
        return self.points[0]

    def last_point(self):
        return self.points[-1]

    def center(self):
        cx = 0
        cy = 0
        cz = 0
        for point in self.points:
            cx += point.x()
            cy += point.y()
            cz += point.z()

        cx = cx/len(self.points)
        cy = cy/len(self.points)
        cz = cz/len(self.points)

        return Point(cx, cy, cz)

    def translate(self, dx, dy):
        self.__transform__(transformations.translate(dx, dy))

    def scale(self, sx, sy):
        self.__transform__(transformations.scale(sx, sy))

    def rotate(self, degrees, center):
        first_translate = transformations.translate(-center.x(), -center.y())
        rotate = transformations.rotate(degrees)
        last_translate = transformations.translate(center.x(), center.y())

        # Concatena as três operações em uma só
        transformation = transformations.concat(transformations.concat(first_translate, rotate), last_translate)

        self.__transform__(transformation)

    def __transform__(self, transformation):
        new_points = []
        for point in self.points:
            result = transformations.concat(point.to_array(), transformation)
            new_points.append(Point(result[0], result[1], result[2]))
        self.set_points(new_points)
