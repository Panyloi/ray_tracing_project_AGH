from math import sqrt
from os import close
from modules.shape import Sphere
from modules.constants import ASPECT_RATIO, HEIGHT, WIDTH, BLACK, random_number, MAX_DEPTH
from modules.hittable import HitRecord, Hittable, HittableList
from modules.imageSaver import Image, image_to_viewport
from modules.vec3 import *
from modules.ray import Ray
from modules.light import LightList, Light
from modules.camera import Camera
from threading import Thread
import time

# aliasing
color = Vec3
point3 = Vec3


# setting background
def reflect_ray(R: Vec3, N: Vec3):
    return N * 2 * N.dot(R) - R


def random_in_unit_sphere():
    while 1:
        rand_vec3 = Vec3.random(-1, 1)
        if rand_vec3.length() ** 2 >= 1: continue
        return rand_vec3


def random_unit_vector():
    rand_vec3 = random_in_unit_sphere()
    return rand_vec3.normalized()


def random_in_hemisphere(normal: Vec3):
    in_unit_sphere = random_in_unit_sphere()
    if in_unit_sphere.dot(normal) > 0.0:
        return in_unit_sphere
    else:
        return in_unit_sphere * (-1)


def ray_color(r: Ray, world, depth: int):
    rec = HitRecord()
    if depth <= 0:
        return color(0, 0, 0)

    is_world_hit, rec, sphere_color, closest_t = world.hit(r, 0.001, float("inf"), rec)
    if is_world_hit:
        target = rec.p + random_in_hemisphere(rec.normal)
        return (rec.normal + color(1, 1, 1)) * 0.5
        r = Ray(rec.p, target - rec.p)
        return ray_color(r, world, depth - 1)
        
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
    local_color = closest_sphere.sphere_color * light.compute_lighting(P, N, world, r.dir * (-1), closest_sphere.specular)
    
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
    image = Image(samples_per_pixel=4)

    # world
    world = HittableList()
    # world.add(Sphere(point3(0,0,-1), 0.5))
    # world.add(Sphere(point3(0,-100.5,-1), 100))
    # ----------------------------------
    world.add(Sphere(point3(0, -1, -3), 1, sphere_color= color(1, 0, 0), reflective=0.3, specular=1000))
    world.add(Sphere(point3(2, 0, -4), 1, sphere_color = color(0, 0, 1), reflective=0.7, specular= 300))
    world.add(Sphere(point3(-2, 0, -4), 1, sphere_color = color(0, 1, 0), reflective=0.1, specular= 100))
    # ground
    world.add(Sphere(point3(0, -5001, 0), 5000, sphere_color=color(1, 1, 0)))
    
    # ----------------------------------
    # world.add(Sphere(point3(0,-100.5,-1), 100, sphere_color=color(0.8, 0.8, 0.0)))
    # world.add(Sphere(point3(0,0,-1), 0.5, sphere_color=color(0.1, 0.2, 0.5)))
    # world.add(Sphere(point3(1.0, 0.0, -1.0), 0.5, sphere_color=color(0.8, 0.6, 0.2)))


    # light
    light = LightList()
    light.add(Light("ambient", intensity=0.4))
    light.add(Light("point", intensity=0.8, position=point3(2, 1, 0)))
    light.add(Light("direction", intensity=0.3, direction=Vec3(1, 4, -4)))

    # camera
    viewport_heigh = 1.0
    viewport_width = ASPECT_RATIO * viewport_heigh
    focal_length = 1.0
    origin = point3(0, 0, 0)
    horizontal = Vec3(viewport_width, 0, 0)
    vertical = Vec3(0, viewport_heigh, 0)
    lower_left_corner = origin - horizontal / 2 - vertical / 2 - Vec3(0, 0, focal_length)
    cam = Camera(point3(0, 0.6, 0))

    # origin = point3(0, 0, 0)
    # horizontal = Vec3(viewport_width, 0, 0)
    # vertical = Vec3(0, viewport_heigh, 0)
    # lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3(0, 0, focal_length)
    threads = []
    number_of_frames = 30
    dt = 360/number_of_frames
    t = 0
    cam = Camera(point3(0,1,3), point3(0, 3, -3), Vec3(0,1,0), 90)
    start_time = time.perf_counter()
    # render
    for k in range(number_of_frames):
        cam.update_camera_pos(t)
        for j in range(HEIGHT - 1, -1, -1):
            print("Scaning remining:{} {}".format(k, j), end = '\r')
            for i in range(WIDTH):
                pixel_color = color()
                for s in range(0, image.samples_per_pixel):

                    u = (i + random_number()) / (WIDTH -1)
                    v = (j + random_number()) / (HEIGHT - 1)
                    r = cam.get_ray(u, v)
                    # pixel_color = ray_color(r, world)
                    pixel_color += trace_ray(r, world, light)

                image.write_color((j, i), pixel_color)  # some modulo staff
        t += dt
        print("\nWhole time to execute: {}".format(time.perf_counter() - start_time))
        # cuboid2 = shape.Cuboid(900, 900, 0, 150, 100).updatePixelMap(image, color=Vec3(128, 255, 0))
        image.save("gif_folder/render{}.ppm".format(k))

# UWAGI
# przy mnożeniu przez sklara Vec3 -> scalar musi być po prawej stronie bo python krzyczy błąd TypeError: unsupported operand type(s) for *: 'float' and 'Vec3'
