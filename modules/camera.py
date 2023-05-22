from modules.vec3 import *
from modules.constants import *
from modules.ray import Ray
import math

class Camera:
    aspect_ratio = 16.0 / 16.0
    viewport_width = 1.0
    viewport_heigh = aspect_ratio * viewport_width
    focal_length = 1.0

    def __init__(
        self,
        lookfrom=point3(),
        lookat = point3(),
        vup = Vec3(),
        vfov = 90, # vertical field-of-view in degrees
        horizontal=Vec3(viewport_width, 0.0, 0.0),
        vertical=Vec3(0.0, viewport_heigh, 0.0),
        lower_left_corner= None,
    ) -> None:

        theta = degrees_to_radians(vfov)
        h = math.tan(theta/2)
        self.viewport_heigh = 2.0 * h
        self.viewport_width = self.aspect_ratio * self.viewport_heigh
        self.lookat = lookat
        self.vup = vup


        self.w = (lookfrom - lookat).normalized()
        self.u = vup.cross(self.w).normalized()
        self.v = self.w.cross(self.u)

        self.origin = lookfrom
        self.horizontal = self.viewport_width * self.u
        self.vertical = self.viewport_heigh * self.v

        if lower_left_corner is not None:
            self.lower_left_corner = lower_left_corner
        else:
            self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical - self.w
        # self.lower_left_corner = lower_left_corner if lower_left_corner is not None\
        #                                            else origin - horizontal/2 - vertical - Vec3(0.0, 0.0, self.focal_length)
        
        self.O = Vec3(lookat.x, lookat.z)
        self.P = Vec3(lookfrom.x, lookfrom.z)
        self.R = (self.O - self.P).length()
        moved_point = Vec3(self.O.x, self.P.x)

        if (moved_point.length() * (self.O - self.P).length()) == 0:
            if self.O.y < 0 or self.P.y < 0:
                self.reallocate_angle =  math.pi
            else:
                self.reallocate_angle = 0
        else:
            self.reallocate_angle = math.acos(moved_point.dot(self.O-self.P) \
                                            / (moved_point.length() * (self.O - self.P).length()))


    def get_ray(self, s: float, t: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin)

    # drawning circle
    def update_camera_pos(self, alpha):
        print()
        print(self.origin, alpha, self.reallocate_angle)
        
        x = self.R * math.sin(degrees_to_radians(alpha) + self.reallocate_angle)
        y = self.R * math.cos(degrees_to_radians(alpha) + self.reallocate_angle)

        new_point = Vec3(x, y)
        new_point += self.O

        self.origin.x = new_point.x
        self.origin.z = new_point.y

        self.w = (self.origin - self.lookat).normalized()
        self.u = self.vup.cross(self.w).normalized()
        self.v = self.w.cross(self.u)


        self.horizontal = self.viewport_width * self.u
        self.vertical = self.viewport_heigh * self.v


        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical - self.w
    