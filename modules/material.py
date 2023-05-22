from modules.vec3 import Vec3
from modules.ray import Ray

def random_in_unit_sphere():    
    while 1:
        rand_vec3 = Vec3.random(-1,1)
        if rand_vec3.length()**2 >= 1: continue
        return rand_vec3
        

def random_unit_vector():
    rand_vec3 = random_in_unit_sphere()
    return rand_vec3.normalized()


def random_in_hemisphere(normal :Vec3):
    in_unit_sphere = random_in_unit_sphere()
    if in_unit_sphere.dot(normal) > 0.0:
        return in_unit_sphere
    else:
        return in_unit_sphere*(-1)


class Material:
    def __init__(self, albedo = Vec3(0,0,0)):
        self.albedo = albedo


class Lambertian(Material):
    def __init__(self, albedo = Vec3(0,0,0)):
        super().__init__(albedo)
    
    def scatter(self, r_in, rec, attenuation, scattered):
        scatter_direction = rec.normal + random_unit_vector()
        
        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True

class Metal(Material):
    def __init__(self, albedo = Vec3(0,0,0)):
        super().__init__(albedo)
    
    def scatter(self, r_in, rec, attenuation, scattered):
        unit_vector = r_in.dir.normalized()
        reflected = unit_vector.reflect(unit_vector, rec.normal)
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return scattered.dir.dot(rec.normal) > 0