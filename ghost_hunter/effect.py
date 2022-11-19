from pico2d import *
import random
import game_framework
import game_world


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



class Effect:
    image=None
    def __init__(self,x,y,dir):
        if Effect.image==None:
            Effect.image = load_image('effect.png')
        self.x, self.y, self.dir = x, y, dir*2
        self.a=self.x



    def update(self):
        #self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time #방향*속도*시간

        self.x+=self.dir
        if abs(self.x-self.a)>100:
            game_world.remove(self)



    def draw(self):
        if self.dir>0:
            self.image.clip_draw(0, 0, 96, 164, self.x + 50, self.y)
        else:
            self.image.clip_draw(0, 0, 96, 164, self.x - 50, self.y)

        #draw_rectangle(*self.get_bb())





    def get_bb(self):
        if self.dir>0:
            return self.x +30, self.y - 40, self.x + 70, self.y + 40
        else:
           return self.x - 70, self.y - 40, self.x -30, self.y + 40



    def handle_collision(self, other, group):
        pass

