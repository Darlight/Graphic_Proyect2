"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

math_functions.py
Proposito: Functions for mathematics
"""
from math import tan, pi
from collections import namedtuple



#Named tuples and math functions from Dennis' Github  and
V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])
V4 = namedtuple('Vertex4', ['x', 'y', 'z','w'])
def sum(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element sum
    """
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)


def sub(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element substraction
    """
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element multiplication
    """
    return V3(v0.x * k, v0.y * k, v0.z * k)


def dot(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Scalar with the dot product
    """
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z


def length(v0):
    """
        Input: 1 size 3 vector
        Output: Scalar with the length of the vector
    """
    return (v0.x ** 2 + v0.y ** 2 + v0.z ** 2) ** 0.5


def norm(v0):
    """
        Input: 1 size 3 vector
        Output: Size 3 vector with the normal of the vector
    """
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x / v0length, v0.y / v0length, v0.z / v0length)


def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]

    xs.sort()
    ys.sort()

    xmin = xs[0]
    xmax = xs[-1]
    ymin = ys[0]
    ymax = ys[-1]

    return xmin, xmax, ymin, ymax


def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x,
    )

def reflect(I, N):
  Lm = mul(I, -1)
  n = mul(N, 2 * dot(Lm, N))
  return norm(sub(Lm, n))


def refract(N, I, refractive_index):  # Implementation of Snell's law
    cosi = -max(-1, min(1, dot(I, N)))
    etai = 1
    etat = refractive_index

    if cosi < 0:  # if the ray is inside the object, swap the indices and invert the normal to get the correct result
      cosi = -cosi
      etai, etat = etat, etai
      N = mul(N, -1)

    eta = etai/etat
    k = 1 - eta**2 * (1 - cosi**2)
    if k < 0:
      return V3(1, 0, 0)

    return norm(sum(
      mul(I, eta),
      mul(N, (eta * cosi - k**(1/2)))
    ))

def fresnel(N, I, refractive_index):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    cosi = max(-1, min(1, dot(I, N)))
    etai = 1
    etat = refractive_index

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

    if sint >= 1: # Total Internal Reflection
        return 1

    cost = max(0, 1 - sint * sint) ** 0.5
    cosi = abs(cosi)
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
    return (Rs * Rs + Rp * Rp) / 2




def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y),
    )

    if abs(cz) < 1:
        return -1, -1, -1

    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz

    return w, v, u