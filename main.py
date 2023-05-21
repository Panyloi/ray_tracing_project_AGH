from math import sqrt
from os import close
from modules.shape import Sphere
from modules.constants import ASPECT_RATIO, HEIGHT, WIDTH, BLACK
from modules.hittable import HitRecord, Hittable, HittableList
from modules.imageSaver import Image, image_to_viewport
from modules.vec3 import Vec3
from modules.ray import Ray
from modules.light import LightList, Light

# aliasing
color = Vec3
point3 = Vec3


# setting background
def reflect_ray(R: Vec3, N: Vec3):
    return N * 2 * N.dot(R) - R


def ray_color(r: Ray, world):
    rec = HitRecord()
    is_world_hit, rec, sphere_color = world.hit(r, 0, float("inf"), rec)
    if is_world_hit:
        return (rec.normal + color(1, 1, 1)) * 0.5

    unit_direction = r.get_direction().normalized()
    t = 0.5 * (unit_direction.y + 1.0)
    return color(1.0, 1.0, 1.0) * (1 - t) + color(0.5, 0.7, 1.0) * t


def trace_ray(r: Ray, world, light: LightList, recursion_depth=3):
    rec = HitRecord()
    is_world_hit, rec, closest_sphere, closest_t = world.hit(r, 0.001, float("inf"), rec)
    if closest_sphere is None:
        # unit_direction = r.get_direction().normalized()
        # t = 0.5 * (unit_direction.y + 1.0)
        # return color(1.0, 1.0, 1.0) * (1 - t) + color(0.5, 0.7, 1.0) * t
        return BLACK

    # Compute local color
    P = r.orig + r.dir * closest_t
    N = P - closest_sphere.center
    N = N.normalized()
    local_color = closest_sphere.sphere_color * light.compute_lighting(P, N, world, r.dir * (-1),
                                                                       closest_sphere.specular)
    # return closest_sphere.sphere_color * light.compute_lighting(rec.p, rec.normal, world)

    # If we hit the recursion limit or the object is not reflective, we're done
    ref = closest_sphere.reflective
    if recursion_depth <= 0 or ref <= 0:
        return local_color

    # Compute the reflected color
    R = reflect_ray(r.dir * (-1), N)
    r.orig = P
    r.dir = R
    reflected_color = trace_ray(r, world, light, recursion_depth - 1)

    return local_color * (1 - ref) + reflected_color * ref


if __name__ == "__main__":
    # image
    image = Image()

    # world
    world = HittableList()
    world.add(Sphere(point3(0, -1, -3), 1, sphere_color=color(1, 0, 0), reflective=0.3, specular=1000))
    world.add(Sphere(point3(2, 0, -4), 1, sphere_color=color(0, 0, 1), reflective=0.7, specular=300))
    world.add(Sphere(point3(-2, 0, -4), 1, sphere_color=color(0, 1, 0), reflective=0.1, specular=100))
    # ground
    world.add(Sphere(point3(0, -5001, 0), 5000, sphere_color=color(1, 1, 0)))

    # light
    light = LightList()
    light.add(Light("ambient", intensity=0.2))
    light.add(Light("point", intensity=0.6, position=point3(2, 1, 0)))
    light.add(Light("direction", intensity=0.2, direction=Vec3(1, 4, -4)))

    # camera
    viewport_heigh = 1.0
    viewport_width = ASPECT_RATIO * viewport_heigh
    focal_length = 1.0

    origin = point3(0, 0, 0)
    horizontal = Vec3(viewport_width, 0, 0)
    vertical = Vec3(0, viewport_heigh, 0)
    lower_left_corner = origin - horizontal / 2 - vertical / 2 - Vec3(0, 0, focal_length)

    # render
    for j in range(HEIGHT - 1, -1, -1):
        print("Scaning remining: {}\r".format(j))
        for i in range(WIDTH):
            u = i / (WIDTH - 1)
            v = j / (HEIGHT - 1)
            r = Ray(origin, lower_left_corner + horizontal * u + vertical * v - origin)
            pixel_color = ray_color(r, world)
            # pixel_color = trace_ray(r, world, light)
            image.write_color((j, i), pixel_color)  # some modulo staff

    image.save("test.ppm")
