from pico2d import *



class Cave:
    def __init__(self):
        self.image = load_image('cave.png')

    def draw(self):
        self.image.draw(400, 300)


    def update(self):
        pass
