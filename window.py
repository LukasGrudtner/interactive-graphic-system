import numpy as np


class Window:
    def __init__(self, x_max, y_max):
        self.__identity = np.eye(3, 3)
        self.__x_min = 0
        self.__y_min = 0
        self.__x_max = x_max
        self.__y_max = y_max

    def x_min(self):
        return self.__x_min

    def x_max(self):
        return self.__x_max

    def y_min(self):
        return self.__y_min

    def y_max(self):
        return self.__y_max
