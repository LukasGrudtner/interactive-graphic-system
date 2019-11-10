import numpy as np
import math


def translate(dx, dy, dz):
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [dx, dy, dz, 1]])


def scale(sx, sy, sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def rotate_x(degrees):
    radians = degrees * (math.pi / 180)
    return np.array([[1, 0, 0, 0],
                     [0, math.cos(radians), math.sin(radians), 0],
                     [0, -math.sin(radians), math.cos(radians), 0],
                     [0, 0, 0, 1]])


def rotate_y(degrees):
    radians = degrees * (math.pi / 180)
    return np.array([[math.cos(radians), 0, -math.sin(radians), 0],
                     [0, 1, 0, 0],
                     [math.sin(radians), 0, math.cos(radians), 0],
                     [0, 0, 0, 1]])


def rotate_z(degrees):
    radians = degrees * (math.pi / 180)
    return np.array([[math.cos(radians), math.sin(radians), 0, 0],
                     [-math.sin(radians), math.cos(radians), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def concat(t1, t2):
    return t1.dot(t2)
