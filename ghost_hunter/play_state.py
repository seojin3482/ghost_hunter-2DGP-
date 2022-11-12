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
                hunter.facedir=1
            elif event.key == SDLK_LEFT:
                hunter.dir += 1
                hunter.facedir=-1


cave = None # c로 따지믄 NULL
running = True
hunter=None
team=None


# 초기화
def enter():
    global cave,hunter,team,running
    team=[Ghost()for i in range(5)]
    hunter=Hunter()
    cave=Cave()
    running = True

# finalization code
def exit():
    global cave,hunter,team
    for ghost in team:
        del ghost
    del cave
    del hunter

def update():

    for ghost in team:
        ghost.update()
    hunter.update()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    cave.draw()
    for ghost in team:
        ghost.draw()
    hunter.draw()


def pause():
    pass

def resume():
    pass

