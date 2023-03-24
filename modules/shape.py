import math
from PIL import Image

class Shape:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
        
    def translate(self, dx, dy, dz):
        self.x += dx
        self.y += dy
        self.z += dz
        
    def save_to_ppm(self, filename):
        size = (100, 100) # size of the image
        im = Image.new('RGB', size, (255, 255, 255)) # create a white image
        pixel = im.load() # create the pixel map

        # iterate over the image and color the pixels according to the shape
        for i in range(size[0]):
            for j in range(size[1]):
                if self.contains(i, j):
                    pixel[i, j] = (0, 0, 0) # set the pixel to black

        # save the image to file
        im.save(filename, "PPM")

    def save_to_png(self, filename):
        size = (100, 100) # size of the image
        im = Image.new('RGB', size, (255, 255, 255)) # create a white image
        pixel = im.load() # create the pixel map

        # iterate over the image and color the pixels according to the shape
        for i in range(size[0]):
            for j in range(size[1]):
                if self.contains(i, j):
                    pixel[i, j] = (0, 0, 0) # set the pixel to black

        # save the image to file
        im.save(filename, "PNG")

class Sphere(Shape):
    def __init__(self, x=0, y=0, z=0, radius=1):
        super().__init__(x, y, z)
        self.radius = radius
        
    def contains(self, x, y):
        # calculate the distance between the point and the center of the sphere
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2 + (self.z)**2)
        
        # check if the point is inside the sphere
        return distance <= self.radius

class Cuboid(Shape):
    def __init__(self, x=0, y=0, z=0, width=1, height=1, depth=1):
        super().__init__(x, y, z)
        self.width = width
        self.height = height
        self.depth = depth
        
    def contains(self, x, y):
        # check if the point is inside the cuboid
        return (x >= self.x - self.width/2 and x <= self.x + self.width/2 and
                y >= self.y - self.height/2 and y <= self.y + self.height/2 and
                self.z - self.depth/2 <= 0 and self.z + self.depth/2 >= 0)

