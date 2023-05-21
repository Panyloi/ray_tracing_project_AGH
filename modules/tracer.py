import random
import math
from .hittable import HitRecord, HittableList
from .vec3 import *
from .constants import *
from .shape import Sphere
from .ray import Ray
from .light import *


class Tracer:
    def __init__(self, world: HittableList):
        self.scene = world

    def get_intersection(self, r) -> tuple[Sphere, float]:
        rec = HitRecord()
        closest = 1e20
        return self.scene.hit(r, 0.0001, closest, rec)[2:4]


    def get_radiance(self, r, depth, lights: LightList):
        result = self.get_intersection(r)
        hit_obj: Sphere = result[0]

        U = random.random()
        if depth > 4 and (depth > 20 or U > hit_obj.sphere_color.get_max_val()):
            return Vec3()

        hit_pos = r.orig + r.dir * result[1]
        norm = hit_obj.get_normal(hit_pos)

        if norm.dot(r.dir) > 0:
            norm = norm * -1

        light_sampling = Vec3()

        if EMITTER_SAMPLING:
            for light in self.scene:
                if light.emit.get_max_val() == 0:
                    continue
                light_pos = light.random_point()
                light_direction = (light_pos - hit_pos).normalized()
                ray_to_light = Ray(hit_pos, light_direction)
                light_hit = self.get_intersection(ray_to_light)

                if light == light_hit[0]:
                    wi = light_direction.dot(norm)
                    if wi > 0:
                        srad = 1.5
                        cos_a_max = math.sqrt(
                            1
                            - srad
                            * srad
                            / (hit_pos - light_pos).dot(hit_pos - light_pos)
                        )
                        omega = 2 * math.pi * (1 - cos_a_max)
                        light_sampling += light.emit * wi * omega * (1 / math.pi)

            # for light in lights:
            #     light_pos = light.position
            #     light_direction = light.direction
            #     ray_to_light = Ray(hit_pos, light_direction)
            #     light_hit = self.get_intersection(ray_to_light)

        angle = 2 * math.pi * random.random()
        dist_cen = math.sqrt(random.random())

        if abs(norm.x) > 0.1:
            u = Vec3(0, 1, 0)
        else:
            u = Vec3(1, 0, 0)

        u = u.cross(norm).normalized()
        v = norm.cross(u)
        d = (
            u * math.cos(angle) * dist_cen
            + v * math.sin(angle) * dist_cen
            + norm * math.sqrt(1 - dist_cen * dist_cen)
        ).normalized()

        reflected = self.get_radiance(Ray(hit_pos, d), depth + 1, lights)
        if not EMITTER_SAMPLING or depth == 0:
            return (
                hit_obj.emit
                + hit_obj.sphere_color * light_sampling
                + hit_obj.sphere_color * reflected
            )
        return hit_obj.sphere_color * light_sampling + hit_obj.sphere_color * reflected
