"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

sphere.py
Proposito: Sphere object
"""
from math_functions import norm, sub, sum, dot, mul, length
from math import atan2,acos, pi
from intersect import Intersect

#Circumference Object
class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, direction):
        L = sub(self.center, orig)
        tca = dot(L, direction)
        l = length(L)
        d2 = (l ** 2 - tca ** 2)
        if d2 > self.radius ** 2:
            return None
        thc = (self.radius ** 2 - d2) ** 1 / 2
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        hit = sum(orig, mul(direction, t0))
        normal = norm(sub(hit, self.center))

        u = 1 - (atan2(normal[2],normal[0])/ (2 * pi) + 0.5)
        v = acos(-normal[1]) / pi

        uvs = [u,v]
        return Intersect(
            distance=t0,
            point=hit,
            normal=normal,
            texCoords = uvs,
            sceneObject = self
        ) 