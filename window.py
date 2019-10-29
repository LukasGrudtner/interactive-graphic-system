import numpy as np
from wireframe import Wireframe
import transformations
from point import Point
from curve import Curve, CurveBezier


class Window:
    def __init__(self, x_max, y_max):
        self.__matrix = np.eye(3, 3)
        self.__x_min = 0
        self.__y_min = 0
        self.__x_max = x_max
        self.__y_max = y_max
        self.__objects = []
        self.__wireframe_builder = Wireframe()
        self.__curve_builder = Curve()

    def x_min(self):
        return self.__x_min

    def x_max(self):
        return self.__x_max

    def y_min(self):
        return self.__y_min

    def y_max(self):
        return self.__y_max

    def builder(self):
        return self.__wireframe_builder

    def curve_builder(self):
        return self.__curve_builder

    def get_object(self, index):
        if len(self.__objects) > index >= 0:
            return self.__objects[index]

    def create_object(self):
        self.__objects.append(self.__wireframe_builder)
        del self.__wireframe_builder
        self.__wireframe_builder = Wireframe()
        return self._self.Gx().shape_objects[-1]

    def create_curve(self):
        self.__objects.append(self.__curve_builder)
        del self.__curve_builder
        self.__curve_builder = CurveBezier()
        return self.__objects[-1]

    def add_object(self, object):
        self.__objects.append(object)

    def objects(self):
        return self.__objects

    def center(self):
        cx = (self.__x_max - self.__x_min)/2
        cy = (self.__y_max - self.__y_min)/2

        return Point(cx, cy, 1)

    def panning_up(self, step):
        abs_step = (self.y_max() - self.y_min()) * (step / 100)
        panning_up = transformations.translate(0, -abs_step)
        self.__matrix = transformations.concat(self.__matrix, panning_up)

    def panning_down(self, step):
        abs_step = (self.y_max() - self.y_min()) * (step / 100)
        panning_down = transformations.translate(0, abs_step)
        self.__matrix = transformations.concat(self.__matrix, panning_down)

    def panning_right(self, step):
        abs_step = (self.x_max() - self.x_min()) * (step / 100)
        panning_right = transformations.translate(-abs_step, 0)
        self.__matrix = transformations.concat(self.__matrix, panning_right)

    def panning_left(self, step):
        abs_step = (self.x_max() - self.x_min()) * (step / 100)
        panning_left = transformations.translate(abs_step, 0)
        self.__matrix = transformations.concat(self.__matrix, panning_left)

    def zoom(self, step):
        scale = 1 + step/100
        if scale == 0:
            scale = 0.01

        first_translate = transformations.translate(-self.center().x(), -self.center().y())
        zoom = transformations.scale(scale, scale)
        last_translate = transformations.translate(self.center().x(), self.center().y())

        self.__matrix = transformations.concat(transformations.concat(transformations.concat(self.__matrix, first_translate), zoom), last_translate)

    def rotate(self, degrees):
        first_translate = transformations.translate(-self.center().x(), -self.center().y())
        rotate = transformations.rotate(degrees)
        last_translate = transformations.translate(self.center().x(), self.center().y())

        # Concatena as três operações em uma só
        self.__matrix = transformations.concat(transformations.concat(transformations.concat(self.__matrix, first_translate), rotate), last_translate)

    def transform(self, object):
        new_object = Wireframe()
        for point in object.get_points():
            result = point.to_array().dot(self.__matrix)
            new_object.insert_point(Point(result[0], result[1], result[2]))
        return new_object
