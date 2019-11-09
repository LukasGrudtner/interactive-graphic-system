import numpy as np
from wireframe import Wireframe
import transformations
from point import Point
from curve import Curve, CurveBezier, CurveHermite, CurveBSpline
from surface import SurfaceBezier


class Window:
    def __init__(self, x_max, y_max):
        self._matrix = np.eye(4, 4)
        self._x_min = 0
        self._y_min = 0
        self._x_max = x_max
        self._y_max = y_max
        self._objects = []

    def x_min(self):
        return self._x_min

    def x_max(self):
        return self._x_max

    def y_min(self):
        return self._y_min

    def y_max(self):
        return self._y_max

    def objects(self):
        return self._objects

    def add_object(self, object):
        self._objects.append(object)

    def get_object(self, i):
        if i > self.size():
            return self._objects[i]

    def size(self):
        return len(self._objects)

    def center(self):
        cx = (self._x_max - self._x_min) / 2
        cy = (self._y_max - self._y_min) / 2

        return Point(cx, cy, 1)

    def panning_up(self, step):
        abs_step = (self.y_max() - self.y_min()) * (step / 100)
        panning_up = transformations.translate(0, -abs_step, 0)
        self._matrix = transformations.concat(self._matrix, panning_up)
        # self.transform(panning_up)

    def panning_down(self, step):
        abs_step = (self.y_max() - self.y_min()) * (step / 100)
        panning_down = transformations.translate(0, abs_step, 0)
        self._matrix = transformations.concat(self._matrix, panning_down)
        # self.transform(panning_down)

    def panning_right(self, step):
        abs_step = (self.x_max() - self.x_min()) * (step / 100)
        panning_right = transformations.translate(-abs_step, 0, 0)
        self._matrix = transformations.concat(self._matrix, panning_right)
        # self.transform(panning_right)

    def panning_left(self, step):
        abs_step = (self.x_max() - self.x_min()) * (step / 100)
        panning_left = transformations.translate(abs_step, 0, 0)
        self._matrix = transformations.concat(self._matrix, panning_left)
        # self.transform(panning_left)

    def panning_forward(self, step):
        abs_step = (self.x_max() - self.x_min()) * (step / 100)
        panning_forward = transformations.translate(0, 0, abs_step)
        self._matrix = transformations.concat(self._matrix, panning_forward)
        # self.transform(panning_forward)

    def panning_back(self, step):
        abs_step = (self.x_max() - self.x_min()) * (step / 100)
        panning_back = transformations.translate(0, 0, -abs_step)
        self._matrix = transformations.concat(self._matrix, panning_back)
        # self.transform(panning_back)

    def zoom(self, step):
        scale = 1 + step / 100
        if scale == 0:
            scale = 0.01

        center = self.center()

        first_translate = transformations.translate(-center.x(), -center.y(), -center.z())
        zoom = transformations.scale(scale, scale, scale)
        last_translate = transformations.translate(center.x(), center.y(), center.z())

        self._matrix = transformations.concat(
            transformations.concat(transformations.concat(self._matrix, first_translate), zoom), last_translate)
        # transformation = transformations.concat(transformations.concat(first_translate, zoom), last_translate)
        # self.transform(transformation)

    def rotate_x(self, degrees):
        self._rotate(transformations.rotate_x(degrees))

    def rotate_y(self, degrees):
        self._rotate(transformations.rotate_y(degrees))

    def rotate_z(self, degrees):
        self._rotate(transformations.rotate_z(degrees))

    def _rotate(self, rotate):
        center = self.center()
        first_translate = transformations.translate(-center.x(), -center.y(), -center.z())
        last_translate = transformations.translate(center.x(), center.y(), center.z())

        self._matrix = transformations.concat(
            transformations.concat(transformations.concat(self._matrix, first_translate), rotate), last_translate)
        # transformation = transformations.concat(transformations.concat(first_translate, rotate), last_translate)
        # self.transform(transformation)

    # def transform(self, transformation):
    #     for object in self._objects:
    #         object.transform(transformation)

    def transform(self, object):
        return object.clone().transform(self._matrix)
