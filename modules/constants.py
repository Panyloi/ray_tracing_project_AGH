from modules.vec3 import Vec3
import random

# library for holding all variables that are used in project
BLACK = Vec3(0, 0, 0)
WHITE = Vec3(255, 255, 255)
# ASPECT_RATIO = 16.0 / 9.0
ASPECT_RATIO = 16.0 / 16.0
WIDTH = 256
HEIGHT = 256
# HEIGHT = int(WIDTH / ASPECT_RATIO)

VW = 1  # viewport width
VH = 1  # viewport height
DISTANCE = 1  # distance between canvas and viewport

SAMPLES_PER_PIXEL = 1
EMITTER_SAMPLING = True



# function to return random value between [0, 1) or between [min_val, max_val]
def random_number(min_val: float = 0.0, max_val: float = 1.0) -> float:
    return min_val + (max_val - min_val) * random.random()

def clamp(x, min_val, max_val):
    if x < min_val:
        return min_val
    if x > max_val:
        return max_val
    return x