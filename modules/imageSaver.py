from os.path import sameopenfile
from modules.vec3 import *
from modules.constants import *


class Image:  # resposnisble for creating and managing image
    def __init__(self, filename=None, mcv=255, samples_per_pixel = 1) -> None:
        # self.image_width = image_width
        # self.image_height = image_height
        self.filename = filename
        self.mcv = mcv  # maximum color value
        self.pixelmap = [[WHITE for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.shapes = []
        self.samples_per_pixel = samples_per_pixel

    def save(self, filename):  # opening file to whole class
        self.f = filename
        with open(filename, "w") as self.f:
            self.init_file()
            self.create_image()

    def getPixelMap(self):
        # return image all white -> prepered to draw
        return self.pixelmap

    def init_file(
        self,
    ):  # initializate ppm file -> header, width, height and maximum color value
        self.f.write("P3\n")
        self.f.write(str(WIDTH) + " " + str(HEIGHT) + "\n" + str(self.mcv) + "\n")

    def create_image(self):  # method for creating ppm image
        for j in range(HEIGHT - 1, -1, -1):
            for i in range(WIDTH):
                pixel = (self.pixelmap[j][i]).int()

                self.f.write(
                    str(pixel.x) + " " + str(pixel.y) + " " + str(pixel.z) + "\n"
                )

    # for now it is not used
    def update_map(self, add_points: set, delete_points: set, color: Vec3):
        for i, j in add_points:
            self.pixelmap[i][j] = color

        for i, j in delete_points:
            self.pixelmap[i][j] = WHITE

    def write_color(
        self, cords: tuple[int, int], pixel_color: color
    ):
        r = pixel_color.x
        g = pixel_color.y
        b = pixel_color.z

        # number of samples for each color in RGB to help antyaliasing
        # scale = 1.0 / self.samples_per_pixel
        # r *= scale
        # g *= scale
        # b *= scale


        self.pixelmap[cords[0]][cords[1]] = Vec3(
            256 * clamp(r, 0.0, 0.999), 256 * clamp(g, 0.0, 0.999), 256 * clamp(b, 0.0, 0.999)
        ).int()


def image_to_viewport(pixel_x, pixel_y):
    return Vec3(pixel_x * VW / WIDTH, pixel_y * VH / HEIGHT, DISTANCE)


if __name__ == "__main__":
    ...
    # Image = Image("example.ppm", 1000, 1000)
    # Image.init_file()
    # Image.create_image()
