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
from lights import *
from sphere import *
from obj import *
from color import *
from boundingBox import *


grassMat = Material(texture = Texture('./textures/grass.bmp'))
sandMat = Material(texture = Texture('./textures/sand.bmp'))
waterMat = Material(diffuse = BLUE, spec = 128, ior = 5, matType= TRANSPARENT) 
cactusMat = Material(texture = Texture('./textures/cactus.bmp'))
dirtMat = Material(texture = Texture('./textures/dirt.bmp'))

raymap = Raytracer(500,500)
raymap.clear()

raymap.envmap = Envmap('./textures/sand_env.bmp')
raymap.dir_light = DirectionalLight(direction = V3(0, -1, 0), intensity = 0.85)
raymap.ambient_light = AmbientLight(strength = 0.5)
raymap.point_lights.append(PointLight(position = V3(5,0,0), intensity = 0.5))

raymap.models.append( boundingBox(V3(-3, -4, -16), V3(2, 2, 2) , sandMat ) )  
raymap.models.append( boundingBox(V3(-1, -4, -16), V3(2, 2, 2) , sandMat ) )   
raymap.models.append( boundingBox(V3(1, -4, -16), V3(2, 2, 2) , sandMat ) )     
raymap.models.append( boundingBox(V3(3, -4, -16), V3(2, 2, 2) , sandMat ) )     

raymap.models.append( boundingBox(V3(-3, -4, -18), V3(2, 2, 2) , sandMat ) )   
raymap.models.append( boundingBox(V3(-1, -4, -18), V3(2, 2, 2) , sandMat ) )   
raymap.models.append( boundingBox(V3(1, -4, -18), V3(2, 2, 2) , sandMat ) )    
raymap.models.append( boundingBox(V3(3, -4, -18), V3(2, 2, 2) , sandMat ) )   

raymap.models.append( boundingBox(V3(-3, -4, -20), V3(2, 2, 2) , sandMat ) )    
raymap.models.append( boundingBox(V3(3, -4, -20), V3(2, 2, 2) , sandMat ) ) 


raymap.finish()
