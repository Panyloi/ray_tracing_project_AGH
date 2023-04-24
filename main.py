from math import sqrt
from os import close
from modules.shape import Sphere
from modules.constants import ASPECT_RATIO, HEIGHT, WIDTH
from modules.hittable import HitRecord, Hittable, HittableList
from modules.imageSaver import Image, image_to_viewport
from modules.vec3 import Vec3
from modules.ray import Ray
from modules.light import LightList, Light


# aliasing
color = Vec3
point3 = Vec3


# setting background


def ray_color(r: Ray, world):
    rec = HitRecord()
    is_world_hit, rec, sphere_color = world.hit(r, 0, float("inf"), rec)
    if is_world_hit:
        return (rec.normal + color(1, 1, 1)) * 0.5

    unit_direction = r.get_direction().normalized()
    t = 0.5 * (unit_direction.y + 1.0)
    return color(1.0, 1.0, 1.0) * (1 - t) + color(0.5, 0.7, 1.0) * t


def trace_ray(r: Ray, world, light: LightList):
    rec = HitRecord()
    is_world_hit, rec, closest_sphere = world.hit(r, 0, float("inf"), rec)
    if closest_sphere is None:
        unit_direction = r.get_direction().normalized()
        t = 0.5 * (unit_direction.y + 1.0)
        return color(1.0, 1.0, 1.0) * (1 - t) + color(0.5, 0.7, 1.0) * t
    
    return closest_sphere.sphere_color * light.compute_lighting(rec.p, rec.normal, world)
    

if __name__ == "__main__":
    #:TODO Przetestować działanie klasy shape
    # Dodać potrzebne pola i metody
    # image = Image()
    # sphere1 = shape.Sphere(500, 500, 40, radius=100).updatePixelMap(image)
    # sphere2 = shape.Sphere(250, 250, 40, radius=100).updatePixelMap(image, color=Vec3(255, 0, 255))
    # cuboid1 = shape.Cuboid(750, 750, 0, 50, 50).updatePixelMap(image)

    # image
    image = Image()

    # world
    world = HittableList()
    # world.add(Sphere(point3(0,0,-1), 0.5))
    # world.add(Sphere(point3(0,-100.5,-1), 100))
    world.add(Sphere(point3(0, -1, -3), 1))
    world.add(Sphere(point3(2, 0, -4), 1, sphere_color = color(0, 0, 1)))
    world.add(Sphere(point3(-2, 0, -4), 1, sphere_color = color(0, 1, 0)))
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
    lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3(0, 0, focal_length)

    # render

    for j in range(HEIGHT - 1, -1, -1):
        # print("Scaning remining: {}\r".format(j))
        for i in range(WIDTH):
            u = i / (WIDTH - 1)
            v = j / (HEIGHT - 1)
            r = Ray(origin, lower_left_corner + horizontal * u + vertical * v - origin)
            # pixel_color = ray_color(r, world)
            pixel_color = trace_ray(r, world, light)
            image.write_color((j, i), pixel_color)  # some modulo staff


    # cuboid2 = shape.Cuboid(900, 900, 0, 150, 100).updatePixelMap(image, color=Vec3(128, 255, 0))
    image.save("listing5.ppm")

# UWAGI
# przy mnożeniu przez sklara Vec3 -> scalar musi być po prawej stronie bo python krzyczy błąd TypeError: unsupported operand type(s) for *: 'float' and 'Vec3'
