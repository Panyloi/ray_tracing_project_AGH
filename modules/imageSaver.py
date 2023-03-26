from modules.vec3 import Vec3

class Image: # resposnisble for creating and managing image
    def __init__(self, filename: str = None, image_width = 256, image_height=256, mcv = 255) -> None:
        self.image_width = image_width
        self.image_height = image_height
        self.f = filename
        self.mcv = 255 # maximum color value
        self.pixelmap = [[Vec3(255, 255, 255) for _ in range(self.image_width)] for _ in range(self.image_height)]


    def save(self, filename = None, pixelmap = None): # opening file to whole class
        if self.f is None:
            self.f = open(filename, "w")
        else:
            self.f = open(self.filename, "w")
        self.pixelmap = pixelmap
        self.init_file()
        self.create_image()

    def load(self):
        # return image all white -> prepered to draw
        return self.pixelmap

    def init_file(self): # initializate ppm file -> header, width, height and maximum color value
        self.f.write("P3\n")
        self.f.write(str(self.image_width) + ' ' + str(self.image_height) + '\n' + str(self.mcv) + '\n')
    
    def close_file(self): # method for closing class file
        self.f.close()

    def create_image(self): # method for creating ppm image
        for j in range(self.image_height - 1, -1, -1):
            for i in range(self.image_width):
                pixel =  (self.pixelmap[j][i]).int()

                self.f.write(str(pixel.x) + ' ' + str(pixel.y) + ' ' + str(pixel.z) + '\n')
        self.close_file() # closing used file to write

if __name__ == '__main__':
    Image = Image("example.ppm", 1000, 1000)
    Image.init_file()
    Image.create_image()