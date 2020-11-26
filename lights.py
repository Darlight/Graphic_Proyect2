"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

lights.py
Proposito: Diferentes shaders for the lights
"""
from color import WHITE
from math_functions import V3, norm

class AmbientLight(object):
    def __init__(self, strength = 0, _color = WHITE):
        self.strength = strength
        self.color = _color

class DirectionalLight(object):
    def __init__(self, direction = V3(0,-1,0), _color = WHITE, intensity = 1):
        self.direction = norm(direction)
        self.intensity = intensity
        self.color = _color

class PointLight(object):
    def __init__(self, position = V3(0,0,0), _color = WHITE, intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color
