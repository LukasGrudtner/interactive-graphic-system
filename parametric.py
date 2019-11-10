from sympy import Matrix, symbols


def t():
    return symbols('t')


def s():
    return symbols('s')


def T():
    t = symbols('t')
    return Matrix([[t ** 3, t ** 2, t, 1]])


def S():
    s = symbols('s')
    return Matrix([[s ** 3, s ** 2, s, 1]])
