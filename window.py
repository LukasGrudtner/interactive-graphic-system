import numpy as np
from wireframe import Wireframe
import transformations
from point import Point


class Window:
    def __init__(self, x_max, y_max):
        self.__matrix = np.eye(3, 3)
        self.__x_min = 0
        self.__y_min = 0
        self.__x_max = x_max
        self.__y_max = y_max
        self.__objects = []
        self.__builder = Wireframe()

    def x_min(self):
        return self.__x_min

    def x_max(self):
        return self.__x_max

    def y_min(self):
        return self.__y_min

    def y_max(self):
        return self.__y_max

    def builder(self):
        return self.__builder

    def get_object(self, index):
        if len(self.__objects) > index >= 0:
            return self.__objects[index]

    def create_object(self):
        self.__objects.append(self.__builder)
        del self.__builder
        self.__builder = Wireframe()
        return self.__objects[-1]

    def add_object(self, object):
        self.__objects.append(object)

    def objects(self):
        return self.__objects

    def panning_up(self, step):
        abs_step = (self.y_max() - self.y_min()) * (step / 100)
        self.__matrix[2][1] -= abs_step

    def panning_down(self, step):
        abs_step = (self.y_max() - self.y_min()) * (step / 100)
        self.__matrix[2][1] += abs_step

    def panning_right(self, step):
        abs_step = (self.x_max() - self.x_min()) * (step / 100)
        self.__matrix[2][0] -= abs_step

    def panning_left(self, step):
        abs_step = (self.x_max() - self.x_min()) * (step / 100)
        self.__matrix[2][0] += abs_step

    def zoom(self, step):
        self.__matrix[0][0] += step / 100
        self.__matrix[1][1] += step / 100

    def rotate(self, degrees):
        rotate = transformations.rotate(degrees)
        self.__matrix = transformations.concat(self.__matrix, rotate)

    def transform(self, object):
        new_object = Wireframe()
        for point in object.get_points():
            result = point.to_array().dot(self.__matrix)
            new_object.insert_point(Point(result[0], result[1], result[2]))
        return new_object
