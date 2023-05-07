import math
import abc
# from PIL import Image
from modules.vec3 import Vec3
from modules.imageSaver import Image
from modules.constants import *
from modules.ray import Ray
from modules.hittable import HitRecord, Hittable

point3 = Vec3
color = Vec3

class Shape:
    def __init__(self, x=0, y=0, z=0):
        self.center = Vec3(x, y, z)
        self.pixel_map = [[WHITE for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.coords = set()
        
    def __str__(self):
        return f"({self.center.x}, {self.center.y}, {self.center.z})"
        
    # def translate(self, dx, dy, dz):
    def translate(self, other : Vec3):
        self.center += other
    
    def contains(self, x, y): ...

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

class Sphere(Shape, Hittable):
    def __init__(self, center = point3(), radius=1.0, sphere_color = color(1, 0, 0), reflective = 0.3, specular = 10):
        self.center = center
        self.radius = radius
        self.sphere_color = sphere_color
        self.reflective = reflective
        self.specular = specular
        
    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord):
        """
        center : center of the sphere
        radious : radious of the sphere
        r : ray

        return : True if ray intersect with sphere, False if not
        """

        # oc - vector between point and origin of the ray
        # we introduce dot product because of equation that has to be smaller then radoius 
        # sphere equation: x**2 + y**2 + z**2 = r**2
        # ray equation: P(t) = A + b*t, where A : origin of ray, b : direction of ray, t : parameter
        oc = r.get_origin() - self.center
        a = r.get_direction().dot(r.get_direction())
        # b = 2 * oc.dot(r.get_direction())
        half_b = oc.dot(r.get_direction())
        c = oc.dot(oc) - self.radius * self.radius
        # if any ray intersect with sphere
        # previous discriminant = b*b - 4*a*c
        discriminant = half_b * half_b - a*c
        if discriminant < 0:
            return False
        delta_sqrt = math.sqrt(discriminant)

        # nearest intersection of ray and sphere
        closest_t = (-half_b - delta_sqrt) / a
        if closest_t < t_min or closest_t > t_max:
            closest_t = (-half_b + delta_sqrt) / a
            if closest_t < t_min or closest_t > t_max:
                return False
        
        rec.t = closest_t
        rec.p = r.at(rec.t)
        outside_normal = (rec.p - self.center) / self.radius
        rec.set_face_and_normal(r, outside_normal)
        
        return True

    # get center of sphere
    def getCenter(self):
        return self.center

class Cuboid(Shape):
    def __init__(self, x=0, y=0, z=0, width=1, height=1, depth=1):
        super().__init__(x, y, z)
        self.width = width
        self.height = height
        self.depth = depth
        
    def contains(self, x, y):
        # check if the point is inside the cuboid
        return (x >= self.center.x - self.width/2 and x <= self.center.x + self.width/2 and
                y >= self.center.y - self.height/2 and y <= self.center.y + self.height/2 and
                self.center.z - self.depth/2 <= 0 and self.center.z + self.depth/2 >= 0)

