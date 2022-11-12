from pico2d import *
import game_framework
#import item_state
import random
from ghost import Ghost
from hunter import Hunter
from cave import Cave









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

