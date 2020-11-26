"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

main.py
Proposito: Bears built with Raytracing
"""
from color import WHITE

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
MAX_RECURSION_DEPTH = 3

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 0, ior = 1, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.matType = matType
        self.ior = ior
        self.texture = texture