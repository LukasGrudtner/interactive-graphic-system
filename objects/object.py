from methods import transformations
from objects.point import Point
import multiprocessing as mp
from copy import deepcopy


class Object:
    def __init__(self, name=None):
        if name is None:
            name = ""
        self._name = name
        self._wireframes = []
        self._transformation = None

    def set_name(self, name):
        self._name = name

    def name(self):
        return self._name

    def add(self, wireframe):
        self._wireframes.append(wireframe)
        return self

    def pop(self, i):
        if i < self.size():
            self._wireframes.pop(i)

    def get(self, i):
        if i < self.size():
            return self._wireframes[i]

    def wireframes(self):
        return self._wireframes

    def size(self):
        return len(self._wireframes)

    def center(self):
        cx, cy, cz, n = 0, 0, 0, 0
        for wireframe in self._wireframes:
            wc = wireframe.center()
            cx += wc.x()
            cy += wc.y()
            cz += wc.z()
            n += 1
        return Point(cx / n, cy / n, cz / n)

    def translate(self, dx, dy, dz):
        translate = transformations.translate(dx, dy, dz)
        self.transform(translate)

    def scale(self, sx, sy, sz):
        center = self.center()
        first_translate = transformations.translate(-center.x(), -center.y(), -center.z())
        scale = transformations.scale(sx, sy, sz)
        last_translate = transformations.translate(center.x(), center.y(), center.z())
        transformation = transformations.concat(transformations.concat(first_translate, scale), last_translate)
        self.transform(transformation)

    def rotate_x(self, degrees, center):
        rotate = transformations.rotate_x(degrees)
        self._rotate(center, rotate)

    def rotate_y(self, degrees, center):
        rotate = transformations.rotate_y(degrees)
        self._rotate(center, rotate)

    def rotate_z(self, degrees, center):
        rotate = transformations.rotate_z(degrees)
        self._rotate(center, rotate)

    def _rotate(self, center, rotate):
        first_translate = transformations.translate(-center.x(), -center.y(), -center.z())
        last_translate = transformations.translate(center.x(), center.y(), center.z())
        transformation = transformations.concat(transformations.concat(first_translate, rotate), last_translate)
        self.transform(transformation)

    def transform(self, transformation):
        return self.serial_transformation(transformation)

    def serial_transformation(self, transformation):
        for wireframe in self._wireframes:
            wireframe.transform(transformation)
        return self

    def parallel_transformation(self, transformation):
        self._transformation = transformation
        parallel = mp.Pool(mp.cpu_count())
        self._wireframes = parallel.map(self.p_transform, self._wireframes)
        return self

    def p_transform(self, wireframe):
        return wireframe.transform(self._transformation)

    def str(self):
        str = ""
        for wireframe in self._wireframes:
            str += wireframe.str()
            str += "\n"
        return str

    def clone(self):
        return deepcopy(self)
