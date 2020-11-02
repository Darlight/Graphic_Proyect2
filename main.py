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
from tracing import *
from material import *
from math_functions import V3
from light import Light
from sphere import *

raymap = Raytracer(500, 500)
raymap.light = Light(
    position=V3(20, 15, 30),
    intensity=1.4
)
raymap.currentbg_color = BLACK
print("Rendering now...")
raymap.models = [

]
raymap.finish(esteogram=True)
print("Bear plushies done!  \n")