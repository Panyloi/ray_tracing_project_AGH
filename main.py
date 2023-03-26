from modules import shape


if __name__ == '__main__':
    #:TODO Przetestować działanie klasy shape
    # Dodać potrzebne pola i metody
    sphere1 = shape.Sphere(500, 500, 40, radius=100)
    sphere1.save_to_ppm("sphere1.ppm")
