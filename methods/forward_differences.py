from sympy import Matrix
from copy import deepcopy
from objects.point import Point


def E(delta):
    return Matrix([[0, 0, 0, 1],
                   [delta ** 3, delta ** 2, delta, 0],
                   [6 * delta ** 3, 2 * delta ** 2, 0, 0],
                   [6 * delta ** 3, 0, 0, 0]])


def update_matrix(DD):
    matrix = deepcopy(DD)
    n_rows = matrix.shape[0]

    for row in range(0, n_rows - 1):
        updated_row = matrix.row(row) + matrix.row(row + 1)
        matrix.row_del(row)
        matrix = matrix.row_insert(row, updated_row)

    return matrix


def draw_curve(n, DDx, DDy, DDz):
    oldx, Dx, D2x, D3x = DDx[0, 0], DDx[0, 1], DDx[0, 2], DDx[0, 3]
    oldy, Dy, D2y, D3y = DDy[0, 0], DDy[0, 1], DDy[0, 2], DDy[0, 3]
    oldz, Dz, D2z, D3z = DDz[0, 0], DDz[0, 1], DDz[0, 2], DDz[0, 3]

    points = []

    for i in range(n):
        x = oldx + Dx
        Dx += D2x
        D2x += D3x

        y = oldy + Dy
        Dy += D2y
        D2y += D3y

        z = oldz + Dz
        Dz += D2z
        D2z += D3z

        points.append(Point(oldx, oldy, oldz))

        oldx, oldy, oldz = x, y, z

    return points
