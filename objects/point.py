import numpy as np
from methods import transformations


class Point:
    def __init__(self, x, y, z, id=-1):
        self._id = id
        self._coordinate = np.array([x, y, z, 1])

    def id(self):
        return self._id

    def x(self):
        return self._coordinate[0]

    def y(self):
        return self._coordinate[1]

    def z(self):
        return self._coordinate[2]

    def coordinate(self):
        return self._coordinate

    def transform(self, transformation):
        self._coordinate = transformations.concat(self._coordinate, transformation)
        return self

    def update(self, coordinate):
        self._coordinate = coordinate

    def str(self):
        return "[" + str(self.x()) + \
               ", " + str(self.y()) + \
               ", " + str(self.z()) + "]"

