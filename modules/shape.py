import math
# from PIL import Image
from modules.vec3 import Vec3
from modules.imageSaver import Image

class Shape:
    def __init__(self, x=0, y=0, z=0):
        # self.x = x
        # self.y = y
        # self.z = z
        self.position = Vec3(x, y, z)
        
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
        
    # def translate(self, dx, dy, dz):
    def translate(self, other : Vec3):
        # self.x += dx
        # self.y += dy
        # self.z += dz
        self.position += other
        
    def save_to_ppm(self, filename):
        size = (1000, 1000) # size of the image
        # im = Image.new('RGB', size, (255, 255, 255)) # create a white image
        im = Image(image_width=size[0], image_height=size[1]) # create a white image
        # pixel = im.load() # create the pixel map
        pixel = im.load() # create the pixel map

        # iterate over the image and color the pixels according to the shape
        for i in range(size[0]):
            for j in range(size[1]):
                if self.contains(i, j):
                    # pixel[i, j] = (0, 0, 0) # set the pixel to black
                    pixel[i][j] = Vec3(0, 0, 0) # set the pixel to black

        # save the image to file
        # im.save(filename, "PPM")
        im.save(filename, pixel)

    # TODO maybe later implement PNG format :"DDD

    # def save_to_png(self, filename):
    #     size = (100, 100) # size of the image
    #     im = Image.new('RGB', size, (255, 255, 255)) # create a white image
    #     pixel = im.load() # create the pixel map

    #     # iterate over the image and color the pixels according to the shape
    #     for i in range(size[0]):
    #         for j in range(size[1]):
    #             if self.contains(i, j):
    #                 pixel[i, j] = (0, 0, 0) # set the pixel to black

    #     # save the image to file
    #     im.save(filename, "PNG")
    

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
    def center(self):
        return self.position

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

