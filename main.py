from modules import shape
from modules.imageSaver import Image
from modules.vec3 import Vec3


if __name__ == '__main__':
    #:TODO Przetestować działanie klasy shape
    # Dodać potrzebne pola i metody
    image = Image()
    sphere1 = shape.Sphere(500, 500, 40, radius=100).updatePixelMap(image)
    sphere2 = shape.Sphere(250, 250, 40, radius=100).updatePixelMap(image, color=Vec3(255, 0, 255))
    cuboid = shape.Cuboid(750, 750, 0, 50, 50).updatePixelMap(image)

    image.save("sphere1.ppm")
