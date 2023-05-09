from modules.constants import *
from modules.vec3 import *
from modules.ray import Ray

class Camera:
    aspect_ratio = 16.0 / 16.0
    viewport_width = 1.0
    viewport_heigh = aspect_ratio * viewport_width
    focal_length = 0.6

    def __init__(
        self,
        origin=point3(),
        horizontal=Vec3(viewport_width, 0.0, 0.0),
        vertical=Vec3(0.0, viewport_heigh, 0.0),
        lower_left_corner= None,
    ) -> None:
        self.origin = origin
        self.horizontal = horizontal
        self.vertical = vertical
        if lower_left_corner is not None:
            self.lower_left_corner = lower_left_corner
        else:
            self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical - Vec3(0.0, 0.0, self.focal_length)
        # self.lower_left_corner = lower_left_corner if lower_left_corner is not None\
        #                                            else origin - horizontal/2 - vertical - Vec3(0.0, 0.0, self.focal_length)

    def get_ray(self, u: float, v: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner + self.horizontal * u + self.vertical * v - self.origin)