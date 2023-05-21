import abc
from modules.ray import Ray
from modules.vec3 import Vec3

point3 = Vec3
color = Vec3

class HitRecord:
    p: point3
    normal : Vec3
    t : float # manipulating t we can get requested plane intersected -> parameter for requested t_min and t_max to compare
    # we are using method called ```backface culling``` that uses normal vector to determine face or back of the shape
    front_face : bool

    # we want determine where the ray is by comapring it with direct of normal vector
    def set_face_and_normal(self, r: Ray, outside_normal: Vec3):
        self.front_face = r.get_direction().dot(outside_normal) < 0 # if < 0 -  then ray is outside of the sphere
        self.normal = outside_normal if self.front_face else outside_normal.reversed()



class Hittable:
    @abc.abstractmethod
    def hit(self, r : Ray, t_min: float, t_max: float, rec: HitRecord): 
        ...

class HittableList(Hittable):
    def __init__(self, object = None) -> None:
        self.objects = list() if object is None else list(object)
        self._index = 0

    def clear(self):
        self.objects.clear()
    
    def add(self, object):
        self.objects.append(object)
    
    def hit(self, r : Ray, t_min: float, t_max: float, rec: HitRecord):
        temp_rec = HitRecord()
        hit_anything = False
        closest_t = t_max
        closest_sphere = None 
        
        for object in self.objects:
            if object.hit(r, t_min, closest_t, temp_rec):
                hit_anything = True
                closest_t = temp_rec.t
                rec = temp_rec
                closest_sphere = object
        
        return hit_anything, rec, closest_sphere, closest_t
    
    def intersects(self, r: Ray):
        ...
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self.objects):
            obj = self.objects[self._index]
            self._index += 1
            return obj
        raise StopIteration
            

