import random
import math

N = 2 * 10 ** 5

TwoPi = 2.0 * math.pi

sum = 0.0

for i in range(N):
    x = random.uniform(0, TwoPi)

    fx = math.exp(-x) * math.sin(x)
    pdf = 1 / (TwoPi - 0.0)

    sum += fx / pdf

I = (1 / N) * sum
print(I)
