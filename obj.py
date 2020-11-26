"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

obj.py
Proposito: Clase objeto que carga archivos .obj
"""
import struct
from math import pi,atan2, acos
from math_functions import V3, norm
def color(r, g, b):
    return bytes([b, g, r])


class Obj(object):
    def __init__(self,filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.faces = []
        self.textcoords = []
        self.normals = []
        self.read()


    def read(self):
        for line in self.lines:
                if line:
                    prefix, value = line.split(' ', 1)

                    if prefix == 'v': # vertices
                        self.vertices.append(list(map(float,value.split(' '))))
                    elif prefix == 'f': # Faces
                        self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])
                    elif prefix == 'vt': # coordinatws
                        self.textcoords.append(list(map(float, value.split(' '))))
                    elif prefix == 'vn': #normals
                        self.normals.append(list(map(float, value.split(" "))))



class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, "rb")
        image.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(2 + 4 + 4 + 4 + 4)

        self.width = struct.unpack("=l", image.read(4))[0]  
        self.height = struct.unpack("=l", image.read(4))[0] 
        self.pixels = []
        image.seek(header_size)

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.pixels[y].append(color(r,g,b))
        image.close()
    
    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        try:
            return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, self.pixels[y][x]))
        except:
            pass  

class Envmap(object):
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        image = open(self.path, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) 
                g = ord(image.read(1)) 
                r = ord(image.read(1))
                self.pixels[y].append(color(r,g,b))

        image.close()

    def getColor(self, direction):

        direction = norm(direction)

        x = int( (atan2( direction[2], direction[0]) / (2 * pi) + 0.5) * self.width)
        y = int(acos(-direction[1]) / pi * self.height )

        return self.pixels[y][x]


