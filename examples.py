from wireframe import Wireframe


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
