from wireframe import Wireframe

VERTEX_DIRECTIVE = 'v'
NAME_DIRECTIVE = 'o'


def read_obj(file):
    file = open(file, 'r')
    object = Wireframe()

    for line in file:
        _handle_line(line.split(" "), object)

    file.close()
    return object


def _handle_line(line, object):
    if len(line) > 0:
        if line[0] == NAME_DIRECTIVE:
            object.set_name(str(line[1]).strip())
        elif line[0] == VERTEX_DIRECTIVE:
            object.add_point(float(line[1]), float(line[2]), float(line[3]))


def write_obj(file, object):
    file = open(file, 'w+')
    file.write("o " + object.get_name() + "\n")
    for point in object.get_points():
        file.write("v ")
        file.write(str(float(point.x())) + " ")
        file.write(str(float(point.y())) + " ")
        file.write(str(float(point.z())) + "\n")
    file.close()
