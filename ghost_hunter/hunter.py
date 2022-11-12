from pico2d import *



class Hunter:
    def __init__(self):
        self.x, self.y = 400, 160
        self.frame = 0
        self.frame2 =0
        self.dir = 0  # 오른쪽
        self.facedir=1
        self.image = load_image('hunter.png')

    def update(self):
        self.frame = (self.frame + 1) % 3+6
        self.frame2 = (self.frame2 + 1) % 6
        self.x += self.dir * 8
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 113, 569, 113, 113, self.x, self.y)
            delay(0.01)

        elif self.dir ==-1:
            self.image.clip_composite_draw(self.frame * 113, 569, 113, 133, -3.141592, 'v', self.x, self.y, 113, 113)
            delay(0.01)

        else:
            if self.facedir==1:
                self.image.clip_composite_draw(0, 565, 113, 133, -3.141592, 'v', self.x, self.y,113,113)

            else:
                self.image.clip_draw(0,565,113,133,self.x,self.y,113,113)


