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
from collections import namedtuple
from math_functions import *
from color import color
from light import Light

#Structures from the Bitmap Render
def char(c):
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    return struct.pack("=h", w)


def dword(d):
    return struct.pack("=l", d)


#Colors
BLACK = color(0, 0, 0)
PURPLISH = color(255, 204, 204)
WHITE = color(255, 255, 255)




#Raymap
class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.models = []
        self.currentbg_color = WHITE
        self.light = None
        self.clear()
        

    def clear(self):
        self.pixels = [[self.currentbg_color for x in range(self.width)] for y in range(self.height)]

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
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y].toBytes())
        f.close()

    def finish(self, filename="plushies.bmp",esteogram=False):
        self.render(esteogram)
        self.write(filename)

    def point(self, x, y, c=None):
        try:
            self.pixels[y][x] = c or self.current_color
        except:
            pass

    def cast_ray(self, orig, direction):
        material, intersect = self.scene_intersect(orig, direction)

        if material is None:
            return self.currentbg_color

        light_dir = norm(sub(self.light.position, intersect.point))
        light_distance = length(sub(self.light.position, intersect.point))

        offset_normal = mul(intersect.normal, 1.1)  # avoids intercept with itself
        shadow_orig = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
        shadow_intensity = 0

        if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
            shadow_intensity = 0.9

        intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

        reflection = reflect(light_dir, intersect.normal)
        specular_intensity = self.light.intensity * (
        max(0, -dot(reflection, direction))**material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
        return (diffuse + specular)

    
    def scene_intersect(self, orig, direction):
        zbuffer = float('inf')

        material = None
        intersect = None

        for obj in self.models:
            hit = obj.ray_intersect(orig, direction)
            if hit is not None:
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = obj.material
                    intersect = hit
        
        return material, intersect


    def render(self,esteoragram=False):
        fov = int(pi / 2)
        for y in range(self.height):
            for x in range(self.width):
                i = (
                    (2 * (x + 0.5) / self.width - 1)
                    * tan(fov / 2)
                    * self.width
                    / self.height
                )
                j = (2 * (y + 0.5) / self.height - 1) * tan(fov / 2)
                direction = norm(V3(i, j, -1))
                if(esteoragram):
                    eye1 = self.cast_ray(V3(0.4,0,0), direction)
                    eye2 = self.cast_ray(V3(-0.4,0,0), direction)
                    if not eye1.equals(self.currentbg_color):
                        eye1 = eye1*0.57 + color(100,0,0)                                          #times 0.57 for it to not exceed 255 
                    if not eye2.equals(self.currentbg_color):
                        eye2 = eye2*0.57 + color(0,0,100)                                          #times 0.57 for it to not exceed 255  
                    eye_sum = eye1 + eye2
                    self.pixels[y][x] = eye_sum
                else:
                    self.pixels[y][x] = self.cast_ray(V3(1,0,0), direction)