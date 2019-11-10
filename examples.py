from wireframe import Wireframe
from curve import *
from surface import SurfaceBezier, SurfaceBSpline
from object import Object
import obj_module as obj


def square():
    wireframe = Wireframe()
    p1 = wireframe.add_point(0, 0, 0)
    p2 = wireframe.add_point(0, 10, 0)
    p3 = wireframe.add_point(10, 10, 0)
    p4 = wireframe.add_point(10, 0, 0)

    wireframe.line(p1, p2)
    wireframe.line(p2, p3)
    wireframe.line(p3, p4)
    wireframe.line(p4, p1)

    square = Object('square')
    square.add(wireframe)

    return square


def cube():
    wireframe = Wireframe()
    p1 = wireframe.add_point(0, 0, 0)
    p2 = wireframe.add_point(10, 0, 0)
    p3 = wireframe.add_point(10, 0, 10)
    p4 = wireframe.add_point(10, 10, 0)
    p5 = wireframe.add_point(10, 10, 10)
    p6 = wireframe.add_point(0, 10, 10)
    p7 = wireframe.add_point(0, 10, 0)
    p8 = wireframe.add_point(0, 0, 10)

    wireframe.line(p1, p2)
    wireframe.line(p1, p7)
    wireframe.line(p1, p8)
    wireframe.line(p2, p3)
    wireframe.line(p2, p4)
    wireframe.line(p3, p5)
    wireframe.line(p3, p8)
    wireframe.line(p4, p5)
    wireframe.line(p4, p7)
    wireframe.line(p5, p6)
    wireframe.line(p6, p7)
    wireframe.line(p6, p8)

    cube = Object('cube.obj')
    cube.add(wireframe)

    return cube


def cube_obj():
    return obj.read('examples/cube.obj')


def line():
    wireframe = Wireframe()
    p1 = wireframe.add_point(0, 0, 0)
    p2 = wireframe.add_point(5, 15, 0)
    p3 = wireframe.add_point(5, 30, 10)

    wireframe2 = Wireframe()
    p12 = wireframe2.add_point(10, 0, 0)
    p22 = wireframe2.add_point(15, 15, 0)
    p32 = wireframe2.add_point(15, 30, 10)

    wireframe.line(p1, p2)
    wireframe.line(p2, p3)

    wireframe2.line(p12, p22)
    wireframe2.line(p22, p32)

    line = Object('line')
    line.add(wireframe)
    line.add(wireframe2)

    return line


def curve_bezier():
    bezier = CurveBezierParametric('curve_bezier')
    bezier.add_point(0, 0, 1)
    bezier.add_point(40, 0, 1)
    bezier.add_point(30, 50, 1)
    bezier.add_point(50, 50, 1)
    bezier.add_point(70, 50, 1)
    bezier.add_point(60, 0, 1)
    bezier.add_point(100, 0, 1)
    return bezier.to_object()


def curve_hermite():
    hermite = CurveHermiteParametric('curve_hermite')
    hermite.add_point(0, 4, 1)
    hermite.add_point(8, 0, 1)
    hermite.add_point(8, 0, 1)
    hermite.add_point(4, 0, 1)
    hermite.add_point(0, 4, 1)
    hermite.add_point(8, 0, 1)
    return hermite.to_object()


def curve_bspline():
    bspline = CurveBSplineForwardDifferences('curve_bspline')
    bspline.add_point(40, 0, 1)
    bspline.add_point(0, 20, 1)
    bspline.add_point(0, 60, 1)
    bspline.add_point(40, 80, 1)
    bspline.add_point(80, 60, 20)
    bspline.add_point(80, 20, 20)
    bspline.add_point(40, 0, 1)
    bspline.add_point(0, 20, 1)
    bspline.add_point(0, 60, 1)
    return bspline.to_object()


def bezier_surface():
    bezier_surface = SurfaceBezier('bezier_surface')
    bezier_surface.add_point(0, 0, 0)
    bezier_surface.add_point(0, 3, 4)
    bezier_surface.add_point(0, 6, 3)
    bezier_surface.add_point(0, 10, 0)
    bezier_surface.add_point(3, 2.5, 2)
    bezier_surface.add_point(2, 6, 5)
    bezier_surface.add_point(3, 8, 5)
    bezier_surface.add_point(4, 0, 2)
    bezier_surface.add_point(6, 3, 2)
    bezier_surface.add_point(8, 6, 5)
    bezier_surface.add_point(7, 10, 4.5)
    bezier_surface.add_point(6, 0, 2.5)
    bezier_surface.add_point(10, 0, 0)
    bezier_surface.add_point(11, 3, 4)
    bezier_surface.add_point(11, 6, 3)
    bezier_surface.add_point(10, 9, 0)
    return bezier_surface.to_object()


def bezier_surface_obj():
    return obj.read('examples/bezier_surface.obj')


def bspline_surface():
    bspline_surface = SurfaceBSpline('bspline_surface')
    bspline_surface.add_point(-100, 300, 100)
    bspline_surface.add_point(0, 300, 100)
    bspline_surface.add_point(100, 300, 100)
    bspline_surface.add_point(200, 300, 100)
    bspline_surface.add_point(-100, 300, 200)
    bspline_surface.add_point(0, -200, 200)
    bspline_surface.add_point(100, -200, 200)
    bspline_surface.add_point(200, 300, 200)
    bspline_surface.add_point(-100, 300, 300)
    bspline_surface.add_point(0, -200, 300)
    bspline_surface.add_point(100, -200, 300)
    bspline_surface.add_point(200, 300, 300)
    bspline_surface.add_point(-100, 300, 400)
    bspline_surface.add_point(0, 300, 400)
    bspline_surface.add_point(100, 300, 400)
    bspline_surface.add_point(200, 300, 400)
    return bspline_surface.to_object()

def bspline_surface_obj():
    return obj.read('examples/bspline_surface.obj')

def bspline_surface_25pts():
    bspline_surface = SurfaceBSpline('bspline_surface')
    bspline_surface.add_point(-100, 300, 100)
    bspline_surface.add_point(0, 300, 100)
    bspline_surface.add_point(100, 300, 100)
    bspline_surface.add_point(200, 300, 100)
    bspline_surface.add_point(-100, 300, 200)
    bspline_surface.add_point(0, -200, 200)
    bspline_surface.add_point(100, -200, 200)
    bspline_surface.add_point(200, 300, 200)
    bspline_surface.add_point(-100, 300, 300)
    bspline_surface.add_point(0, -200, 300)
    bspline_surface.add_point(100, -200, 300)
    bspline_surface.add_point(200, 300, 300)
    bspline_surface.add_point(-100, 300, 400)
    bspline_surface.add_point(0, 300, 400)
    bspline_surface.add_point(100, 300, 400)
    bspline_surface.add_point(200, 300, 400)
    bspline_surface.add_point(-100, 300, 300)
    bspline_surface.add_point(0, -200, 300)
    bspline_surface.add_point(100, -200, 300)
    bspline_surface.add_point(200, 300, 300)
    bspline_surface.add_point(-100, 300, 200)
    bspline_surface.add_point(0, -200, 200)
    bspline_surface.add_point(100, -200, 200)
    bspline_surface.add_point(200, 300, 200)
    bspline_surface.add_point(200, 300, 100)
    return bspline_surface.to_object()

def bspline_surface_25pts_obj():
    return obj.read('examples/bspline_surface_25pts.obj')