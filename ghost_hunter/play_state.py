from pico2d import *
import game_framework
#import item_state
import random


class Cave:
    def __init__(self):
        self.image = load_image('cave.png')

    def draw(self):
        self.image.draw(400, 300)

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



class Hunter:
    def __init__(self):
        self.x, self.y = 400, 160
        self.frame = 0
        self.frame2 =0
        self.dir = 0  # 오른쪽
        self.image = load_image('hunter.png')

    def update(self):
        self.frame = (self.frame + 1) % 3+6
        self.frame2 = (self.frame2 + 1) % 6
        self.x += self.dir * 4
        if self.x > 800:
            self.x = 800
            self.dir = 0
        elif self.x < 0:
            self.x = 0
            self.dir = 0

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 113, 569, 113, 113, self.x, self.y)
            delay(0.01)

        elif self.dir==0:
            self.image.clip_draw(0,565,113,133,self.x,self.y)

        else:
            self.image.clip_draw(self.frame2 * 113, 341, 113, 113, self.x, self.y)
            delay(0.01)








def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                hunter.dir += 1
            elif event.key == SDLK_LEFT:
                hunter.dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                hunter.dir -= 1
            elif event.key == SDLK_LEFT:
                hunter.dir += 1


cave = None # c로 따지믄 NULL
ghost =None
ghost2=None
ghost3=None
running = True
hunter=None



# 초기화
def enter():
    global cave,hunter,ghost,ghost2,ghost3,running
    ghost=Ghost()
    ghost2=Ghost()
    ghost3=Ghost()
    hunter=Hunter()
    cave=Cave()
    running = True

# finalization code
def exit():
    global cave,hunter,ghost,ghost2,ghost3
    del ghost
    del ghost2
    del ghost3
    del cave
    del hunter

def update():

    ghost.update()
    ghost2.update()
    ghost3.update()
    hunter.update()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    cave.draw()
    ghost.draw()
    ghost2.draw()
    ghost3.draw()
    hunter.draw()


def pause():
    pass

def resume():
    pass

