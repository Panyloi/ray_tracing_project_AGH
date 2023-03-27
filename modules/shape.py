import math
# from PIL import Image
from modules.vec3 import Vec3
from modules.imageSaver import Image
from modules.constants import *
class Shape:
    def __init__(self, x=0, y=0, z=0):
        self.position = Vec3(x, y, z)
        self.pixel_map = [[WHITE for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.coords = set()
        
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
        
    # def translate(self, dx, dy, dz):
    def translate(self, other : Vec3):
        self.position += other
    
    def updatePixelMap(self, image: Image, 
                       cords: Vec3 = Vec3(0, 0, 0), 
                       color: Vec3 = BLACK):
        # for now its only color and coordinates of center of shape
        points_to_remove = set()
        points_to_add = set()
        self.translate(cords)
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.contains(i, j):
                    # pixel[i, j] = (0, 0, 0) # set the pixel to black
                    self.pixel_map[i][j] = color # set the pixel to black
                    if (i, j) not in self.coords:
                        self.coords.add((i, j))
                        points_to_add.add((i, j))
                else:
                    if (i, j) in self.coords:
                        self.coords.remove((i, j))
                        points_to_remove.add((i, j))
                    self.pixel_map[i][j] = WHITE

        # update main map of shapes
        image.update_map(points_to_add, points_to_remove, color)


    def saveShapeToPixelMap(self):
        ...

    # TODO maybe later implement PNG format :"DDD

class Sphere(Shape):
    def __init__(self, x=0, y=0, z=0, radius=1):
        super().__init__(x, y, z)
        self.radius = radius
        
    def contains(self, x, y):
        # calculate the distance between the point and the center of the sphere
        distance = math.sqrt((x - self.position.x)**2 + (y - self.position.y)**2 + (self.position.z)**2)
        
        # check if the point is inside the sphere
        return distance <= self.radius

    # get center of sphere
    def getCenter(self):
        return self.position

class Cuboid(Shape):
    def __init__(self, x=0, y=0, z=0, width=1, height=1, depth=1):
        super().__init__(x, y, z)
        self.width = width
        self.height = height
        self.depth = depth
        
    def contains(self, x, y):
        # check if the point is inside the cuboid
        return (x >= self.position.x - self.width/2 and x <= self.position.x + self.width/2 and
                y >= self.position.y - self.height/2 and y <= self.position.y + self.height/2 and
                self.position.z - self.depth/2 <= 0 and self.position.z + self.depth/2 >= 0)

