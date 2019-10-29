from wireframe import Wireframe
from curve import Curve, CurveBezier, CurveHermite


def square():
    gen_square = Wireframe()
    gen_square.set_name("square")
    gen_square.add_point(0, 0, 0)
    gen_square.add_point(0, 100, 0)
    gen_square.add_point(100, 100, 0)
    gen_square.add_point(100, 0, 0)
    return gen_square


def line():
    gen_line = Wireframe()
    gen_line.set_name("line")
    gen_line.add_point(0, 0, 0)
    gen_line.add_point(50, 150, 0)
    return gen_line


def curve_bezier():
    gen_curve = CurveBezier()
    gen_curve.set_name("curve_bezier")
    gen_curve.add_point(0, 0, 1)
    gen_curve.add_point(400, 0, 1)
    gen_curve.add_point(300, 500, 1)
    gen_curve.add_point(500, 500, 1)
    gen_curve.add_point(700, 500, 1)
    gen_curve.add_point(600, 0, 1)
    gen_curve.add_point(1000, 0, 1)
    return gen_curve


def curve_hermite():
    gen_curve = CurveHermite()
    gen_curve.set_name("curve_hermite")
    gen_curve.add_point(0, 400, 1)
    gen_curve.add_point(800, 0, 1)
    gen_curve.add_point(800, 0, 1)
    gen_curve.add_point(400, 0, 1)
    gen_curve.add_point(0, 400, 1)
    gen_curve.add_point(800, 0, 1)
    # gen_curve.add_point(400, 400, 1)
    # gen_curve.add_point(800, 0, 1)
    # gen_curve.add_point(1000, 0, 1)
    return gen_curve
