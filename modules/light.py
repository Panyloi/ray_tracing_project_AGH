from modules.vec3 import Vec3
from modules.ray import Ray
from modules.hittable import HitRecord, HittableList

point3 = Vec3
color = Vec3

class Light:
    def __init__(self, type : str, intensity : float = 0.0, direction : Vec3 = Vec3(), position : point3 = point3()) -> None:
        self.type = type
        self.intensity = intensity
        self.direction = direction
        self.position = position

class LightList:
    def __init__(self, object = None) -> None:
        self.lights = list() if object is None else list(object)
    
    def clear(self):
        self.lights.clear()
    
    def add(self, object):
        self.lights.append(object)
    
    # P - point where ligth and shape intersect
    # N - normal vector from center of shape to P
    def compute_lighting(self, P: point3, N: point3, shapes: HittableList):
        i = 0.0

        for light in self.lights:
            if light.type == "ambient":
                i += light.intensity
            else:
                if light.type == "point":
                    L = light.position - P
                    t_max = 1.0
                else:
                    L = light.direction
                    t_max = float("inf")
                
                # Shadow checking
                tmp_rec = HitRecord()
                hit_anything, rec, shadow_sphere = shapes.hit(Ray(P, L), 0.001, t_max, tmp_rec)
                if shadow_sphere is not None:
                    # print("{}".format(i))
                    continue
                n_dot_l = L.dot(N)
                if n_dot_l > 0:
                    i += light.intensity * n_dot_l/(N.length() * L.length())
        
        return i