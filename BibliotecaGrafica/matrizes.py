import math
def identidade():

    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

def translacao(tx, ty):

    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

def escala(sx, sy):

    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def rotacao(theta):

    c = math.cos(theta)
    s = math.sin(theta)

    return [
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ]

def multiplica_matrizes(a, b):

    r = [[0] * 3 for _ in range(3)]

    for i in range(3):
        for j in range(3):
            for k in range(3):

                r[i][j] += a[i][k] * b[k][j]

    return r