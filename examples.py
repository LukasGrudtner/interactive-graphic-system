from wireframe import Wireframe
from curve import Curve, CurveBezier, CurveHermite, CurveBSpline


def square():
    gen_square = Wireframe()
    gen_square.set_name("square")
    gen_square.add_point(0, 0, 0)
    gen_square.add_point(0, 10, 0)
    gen_square.add_point(10, 10, 0)
    gen_square.add_point(10, 0, 0)
    return gen_square


def line():
    gen_line = Wireframe()
    gen_line.set_name("line")
    gen_line.add_point(0, 0, 0)
    gen_line.add_point(5, 15, 0)
    return gen_line


def curve_bezier():
    gen_curve = CurveBezier()
    gen_curve.set_name("curve_bezier")
    gen_curve.add_point(0, 0, 1)
    gen_curve.add_point(40, 0, 1)
    gen_curve.add_point(30, 50, 1)
    gen_curve.add_point(50, 50, 1)
    gen_curve.add_point(70, 50, 1)
    gen_curve.add_point(60, 0, 1)
    gen_curve.add_point(100, 0, 1)
    return gen_curve


def curve_hermite():
    gen_curve = CurveHermite()
    gen_curve.set_name("curve_hermite")
    gen_curve.add_point(0, 40, 1)
    gen_curve.add_point(80, 0, 1)
    gen_curve.add_point(80, 0, 1)
    gen_curve.add_point(40, 0, 1)
    gen_curve.add_point(0, 40, 1)
    gen_curve.add_point(80, 0, 1)
    # gen_curve.add_point(400, 400, 1)
    # gen_curve.add_point(800, 0, 1)
    # gen_curve.add_point(1000, 0, 1)
    return gen_curve


def curve_bspline_fwd_diff():
    gen_curve = CurveBSpline()
    gen_curve.set_name("curve_b_spline_fwd_diff")
    gen_curve.add_point(40, 0, 1)
    gen_curve.add_point(0, 20, 1)
    gen_curve.add_point(0, 60, 1)
    gen_curve.add_point(40, 80, 1)
    gen_curve.add_point(80, 60, 1)
    gen_curve.add_point(80, 20, 1)
    gen_curve.add_point(40, 0, 1)
    gen_curve.add_point(0, 20, 1)
    gen_curve.add_point(0, 60, 1)
    return gen_curve
