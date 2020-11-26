"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

intersect.py
Proposito: Intersections between points and objects
"""

class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texCoords = texCoords
        self.sceneObject = sceneObject

