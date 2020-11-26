"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

plane.py
Proposito: Plane object
"""
from intersect import Intersect
from math_functions import norm, sub, sum, dot, mul
class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = norm(normal)
        self.material = material

    def ray_intersect(self, orig, dir):
        # t = (( position - origRayo) dot normal) / (dirRayo dot normal)

        #denom = np.dot(dir, self.normal)
        denom = dot(dir,self.normal)

        if abs(denom) > 0.0001:
            t = dot(self.normal, sub(self.position, orig)) / denom
            if t > 0:
                # P = O + tD
                hit = sum(orig, mul(dir, t))

                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal,
                                 texCoords = None,
                                 sceneObject = self)

        return None
