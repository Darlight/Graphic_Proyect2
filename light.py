"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

light.py
Proposito: Light for models
"""
from math_functions import V3

class Light(object):
	def __init__(self, position=V3(0,0,0), intensity=0):
		self.position = position
		self.intensity = intensity