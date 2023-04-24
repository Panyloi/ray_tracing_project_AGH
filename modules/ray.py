from modules.vec3 import Vec3
from modules.constants import *
from modules.imageSaver import image_to_viewport


class Ray:
    def __init__(self, origin: Vec3, direction : Vec3):
        self.orig = origin
        self.dir = direction


    # return origin of the ray
    def get_origin(self) -> Vec3:
        return self.orig
    
    # return direction of the ray
    def get_direction(self) -> Vec3:
        return self.dir

    def at(self, t) -> Vec3:
        return self.orig + self.dir * t
    

    
