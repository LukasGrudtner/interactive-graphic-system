from objects.wireframe import Wireframe
from objects.object import Object

VERTEX_DIRECTIVE = 'v'
NAME_DIRECTIVE = 'o'
LINE_DIRECTIVE = 'l'


def read(file):
    file = open(file, 'r')
    object = Object()

    lines = []
    for line in file:
        lines.append(line)

    it = 0
    while it < len(lines):
        if lines[it].split()[0] == NAME_DIRECTIVE:
            object = Object(str(lines[it].split()[1]).strip())
            points = []
            it += 1
            while it < len(lines):
                if lines[it].split()[0] == VERTEX_DIRECTIVE:
                    wireframe = Wireframe()
                    object.add(wireframe)
                    while it < len(lines):
                        if lines[it].split()[0] == VERTEX_DIRECTIVE:
                            points.append(wireframe.add_point(float(lines[it].split()[1]), float(lines[it].split()[2]),
                                                              float(lines[it].split()[3])))
                            it += 1
                        else:
                            break

                if lines[it].split()[0] == LINE_DIRECTIVE:
                    while it < len(lines):
                        if lines[it].split()[0] == LINE_DIRECTIVE:
                            wireframe.line(wireframe.get_point_by_id(int(lines[it].split()[1])),
                                           wireframe.get_point_by_id(int(lines[it].split()[2])))
                            it += 1
                        else:
                            break
    return object

def write(file, object):
    file = open(file, 'w+')
    file.write(NAME_DIRECTIVE + ' ' + object.name() + '\n')

    for wireframe in object.wireframes():
        _write_points(file, wireframe.points())
        _write_lines(file, wireframe.lines())

    file.close()


def _write_points(file, points):
    for point in points:
        file.write(VERTEX_DIRECTIVE + ' ')
        file.write(str(float(point.x())) + ' ')
        file.write(str(float(point.y())) + ' ')
        file.write(str(float(point.z())) + '\n')


def _write_lines(file, lines):
    for line in lines:
        file.write(LINE_DIRECTIVE + ' ')
        file.write(str(line.p1().id()) + ' ')
        file.write(str(line.p2().id()) + '\n')
