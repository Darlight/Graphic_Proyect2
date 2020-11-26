"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

tracing.py
Proposito: Render of objects via Ray Intersect Algorithm
"""


import struct
from math_functions import *
from color import color, BLACK, WHITE
from material import *
from sphere import *
from plane import Plane
from obj import Obj
from boundingBox import *
from lights import *
#Structures from the Bitmap Render
def char(c):
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    return struct.pack("=h", w)


def dword(d):
    return struct.pack("=l", d)


#Colors
PURPLISH = color(255, 204, 204)




#Raymap
class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.models = []
        self.currentbg_color = WHITE
        self.current_color = PURPLISH
        self.camara_position = V3(0,0,0)
        self.fov = 60
        self.point_lights = []
        self.envmap = None
        self.ambient_light = None
        self.dir_light = None
        self.clear()
        self.viewport(0,0,width,height)
        

    def clear(self):
        self.pixels = [[self.currentbg_color for x in range(self.width)] for y in range(self.height)]
        
        self.zbuffer = [ [ float('inf') for x in range(self.width)] for y in range(self.height) ]



    def write(self, filename):
        f = open(filename, 'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Image header (40 bytes)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Pixel data (width x height x 3 pixels)
        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                f.write(color(depth,depth,depth))

        f.close()



    def finish(self, filename="project2.bmp"):
        self.render()
        self.write(filename)

    def point(self, x, y, c=None):
        try:
            self.pixels[y][x] = c or self.current_color
        except:
            pass

    def viewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

    def vertex_Coord(self, x, y, color = None):
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.current_color
        except:
            pass

    def vertex(self, x, y, color = None):
        pixelX = ( x + 1) * (self.vpWidth  / 2 ) + self.vpX
        pixelY = ( y + 1) * (self.vpHeight / 2 ) + self.vpY

        if pixelX >= self.width or pixelX < 0 or pixelY >= self.height or pixelY < 0:
            return

        try:
            self.pixels[round(pixelY)][round(pixelX)] = color or self.current_color
        except:
            pass

    def cast_ray(self, orig, direction, original_obj = None, recursion = 0):

        material, intersect = self.scene_intersect(orig, direction,original_obj)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envmap:
                return self.envmap.getColor(direction)
            return self.currentbg_color

        colorObject = material.diffuse 

        colorAmbient = V3(0,0,0)
        colorLightDir = V3(0,0,0)
        lightPColor = V3(0,0,0)
        colorReflect = V3(0,0,0)
        colorRefract = V3(0,0,0)
        colorFinal = V3(0,0,0)

        direction_view = norm(sub(self.camara_position, intersect.point))

        if self.ambient_light:
            colorAmbient = V3(((self.ambient_light.strength * self.ambient_light.color[2])/255),
            ((self.ambient_light.strength * self.ambient_light.color[1])/255),
            ((self.ambient_light.strength * self.ambient_light.color[0])/255)) 

        if self.dir_light:
            shadow_intensity = 0
            diffuseColor = V3(0,0,0)
            specColor = V3(0,0,0)

            dir_light = self.dir_light.direction*-1

             # Calculamos el valor del diffuse color.
            intensity = mul(self.dir_light.intensity,(max(0,dot(dir_light, intersect.normal))))
            diffuseColor = V3(intensity * self.dir_light.color[2] / 255,
                                     intensity * self.dir_light.color[1] / 255,
                                     intensity * self.dir_light.color[0] / 255)

            # Iluminacion especular
            reflect = reflect(intersect.normal, dir_light) # Reflejar el vector de luz

            # spec_intensity: lightIntensity * ( view_dir dot reflect) ** especularidad
            spec_intensity = mul(self.dir_light.intensity,(max(0, (dot(direction_view, reflect)) ** material.spec)))
            specColor = V3(spec_intensity * self.dir_light.color[2] / 255,
                                  spec_intensity * self.dir_light.color[1] / 255,
                                  spec_intensity * self.dir_light.color[0] / 255)


            shadMat, shadInter = self.scene_intersect(intersect.point,  dir_light, intersect.sceneObject)
            if shadInter is not None:
                shadow_intensity = 1

            dirLightColor = (1 - shadow_intensity) * (diffuseColor + specColor)
        
        for lightPoint in self.point_lights:
            shadow_intensity = 0
            diffuseColor = V3(0,0,0)
            specColor = V3(0,0,0)

            # Sacamos la direccion de la luz para este punto
            dir_light = norm(sub(lightPoint.position,intersect.point))

            # Calculamos el valor del diffuse color
            intensity = mul(lightPoint.intensity, max(0,dot(dir_light, intersect.normal)))
            diffuseColor = V3(intensity * lightPoint.color[2] / 255,
                                     intensity * lightPoint.color[1] / 255,
                                     intensity * lightPoint.color[0] / 255)

            # Iluminacion especular
            reflect = reflect(intersect.normal, dir_light) # Reflejar el vector de luz

            # spec_intensity: lightIntensity * ( view_dir dot reflect) ** especularidad
            spec_intensity = mul(lightPoint.intensity,(max(0, (dot(direction_view, reflect)) ** material.spec)))
            specColor = V3(spec_intensity * lightPoint.color[2] / 255,
                                  spec_intensity * lightPoint.color[1] / 255,
                                  spec_intensity * lightPoint.color[0] / 255)


            shadMat, shadInter = self.scene_intersect(intersect.point,  dir_light, intersect.sceneObject)
            if shadInter is not None and shadInter.distance < norm(sub(lightPoint.position, intersect.point)):
                shadow_intensity = 1

            lightPColor = sum(lightPColor, ((1 - shadow_intensity) * sum(diffuseColor,specColor)))

        if material.matType == OPAQUE:
            # Formula de iluminacion, PHONG
            finalColor = (colorAmbient + dirLightColor + lightPColor)

            if material.texture and intersect.texCoords:

                texColor = material.texture.getColor(intersect.texCoords[0], intersect.texCoords[1])

                finalColor *= V3(texColor[2] / 255,
                                        texColor[1] / 255,
                                        texColor[0] / 255)


        elif material.matType == REFLECTIVE:
            reflect = reflect(intersect.normal, direction* -1)
            reflectColor = self.cast_ray(intersect.point, reflect, intersect.sceneObject, recursion + 1)
            reflectColor = V3(reflectColor[2] / 255,
                                     reflectColor[1] / 255,
                                     reflectColor[0] / 255)

            finalColor = reflectColor

        elif material.matType == TRANSPARENT:

            outside = dot(direction, intersect.normal) < 0
            bias = 0.001 * intersect.normal
            kr = fresnel(intersect.normal, direction, material.ior)

            reflect = reflect(intersect.normal, direction * -1)
            reflectOrig = sum(intersect.point, bias) if outside else sub(intersect.point, bias)
            reflectColor = self.cast_ray(reflectOrig, reflect, None, recursion + 1)
            reflectColor = V3(reflectColor[2] / 255,
                                     reflectColor[1] / 255,
                                     reflectColor[0] / 255)

            if kr < 1:
                refract = refract(intersect.normal, direction, material.ior)
                refractOrig = sub(intersect.point, bias) if outside else sum(intersect.point, bias)
                refractColor = self.cast_ray(refractOrig, refract, None, recursion + 1)
                refractColor = V3(refractColor[2] / 255,
                                         refractColor[1] / 255,
                                         refractColor[0] / 255)

            finalColor = reflectColor * kr + refractColor * (1 - kr)

        # Le aplicamos el color del objeto
        finalColor *= colorObject

        #Nos aseguramos que no suba el valor de color de 1
        r = min(1,finalColor[0])
        g = min(1,finalColor[1])
        b = min(1,finalColor[2])
        
        return color(r, g, b)
    



    
    
    def scene_intersect(self, orig, direction, original_obj = None):
        zbuffer = float('inf')

        material = None
        intersect = None

        for obj in self.models:
            if obj is not original_obj:    
                hit = obj.ray_intersect(orig, direction)
                if hit is not None:
                    if hit.distance < zbuffer:
                        zbuffer = hit.distance
                        material = obj.material
                        intersect = hit
        
        return material, intersect


    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                i = (
                    (2 * (x + 0.5) / self.width - 1)
                    * tan(self.fov / 2)
                    * self.width
                    / self.height
                )
                j = (2 * (y + 0.5) / self.height - 1) * tan(self.fov / 2)
                direction = norm(V3(i, j, -1))
                self.vertex_Coord(x,y,self.cast_ray(self.camara_position, direction))