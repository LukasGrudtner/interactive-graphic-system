import numpy as np
import math


def translate(dx, dy):
    return np.array([[1, 0, 0],
                     [0, 1, 0],
                     [dx, dy, 0]])


def scale(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])


def rotate(degrees):
    radians = degrees * (math.pi/180)
    return np.array([[math.cos(radians), -math.sin(radians), 0],
                     [math.sin(radians), math.cos(radians), 0],
                     [0, 0, 1]])


def concat(t1, t2):
    return t1.dot(t2)
