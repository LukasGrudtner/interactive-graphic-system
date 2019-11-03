import numpy as np


class Point:
    def __init__(self, x, y, z):
        self.__teste123 = x
        self.coordinate = np.array([x, y, z, 1])

    def x(self):
        return self.coordinate[0]

    def y(self):
        return self.coordinate[1]

    def z(self):
        return self.coordinate[2]

    def to_string(self):
        return "[" + str(self.x()) + \
               ", " + str(self.y()) + \
               ", " + str(self.z()) + "]"

    def to_array(self):
        return self.coordinate
