from pico2d import *
import random


class Ghost:
    def __init__(self):
        self.x, self.y = random.randint(0,800), 160
        self.frame = 0
        self.frame2 = 0
        self.dir = 1 # 오른쪽
        self.image = load_image('ghost.png')


    def update(self):
        self.frame = (self.frame + 1) % 4+4
        self.frame2 = (self.frame2 + 1) % 4
        self.x += self.dir * 1
        if self.x > 800:
            self.x = 800
            self.dir = -1 #왼쪽
        elif self.x < 0:
            self.x = 0
            self.dir = 1


    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame*144, 128, 144, 128,self.x, self.y)
            delay(0.01)

        else:

            self.image.clip_draw(self.frame2*144, 128, 144, 128, self.x, self.y)
            delay(0.01)



