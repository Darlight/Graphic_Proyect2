"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

intersect.py
Proposito: Intersection between models
"""
class Intersect(object):
	def __init__(self, distance, point, normal):
		self.distance = distance
		self.point = point
		self.normal = normal