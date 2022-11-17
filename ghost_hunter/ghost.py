from pico2d import *
import random
import game_framework


# Ghost Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Ghost action Speed (frame)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_RUN = 4



class Ghost:
    def __init__(self):
        self.x, self.y = random.randint(0,800), 160
        self.frame = 0
        self.frame2 = 0
        self.dir = 1 # 오른쪽
        self.image = load_image('ghost.png')


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 4+4
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time #방향*속도*시간
        if self.x > 800:
            self.x = 800
            self.dir = -1 #왼쪽
        elif self.x < 0:
            self.x = 0
            self.dir = 1


    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame)*144, 128, 144, 128,self.x, self.y)
        else:
            self.image.clip_composite_draw(int(self.frame)*144, 128, 144, 128, -3.141592, 'v', self.x, self.y, 144, 128)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40


