from modules import shape

if __name__ == '__main__':
    sh = shape.Shape(2,5,7)
    sph = shape.Sphere(sh)
    print(sh.__str__())
