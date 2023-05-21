from math import sqrt
import random

class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0) -> None:
        if isinstance(x, Vec3):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        else:
            self.x = x
            self.y = y
            self.z = z

    def tuple(self):
        return (self.x, self.y, self.z)

    def reversed(self):
        return Vec3(-self.x, -self.y, -self.z)

    def copy(self, other):
        return Vec3(self.x, self.y, self.z)

    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def int(self):
        return Vec3(int(self.x), int(self.y), int(self.z))

    def normalize(self):
        l = self.length()

        if l == 0:
            return self

        self.x /= l
        self.y /= l
        self.y /= l

        return self

    def normalized(self):
        l = self.length()

        if l == 0:
            return Vec3()

        return Vec3(self.x / l, self.y / l, self.z / l)

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def random(min: float, max: float):
        return Vec3(random.uniform(min,max), random.uniform(min,max), random.uniform(min,max))
    

    def near_zero(self):
        # Return True if the vector is close to zero in all dimensions.
        s = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s


    def reflect(self, other):
        return self - self.dot(other)*2*other


    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __abs__(self):
        return Vec3(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self

    def __idiv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self
    
    def __repr__(self):
        return repr((self.x, self.y, self.z))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

point3 = Vec3
color = Vec3


if __name__ == '__main__':
    vector = Vec3(1.20, 2, 3)


