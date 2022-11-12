from pico2d import *
import game_framework
#import item_state
import random
from ghost import Ghost
from hunter import Hunter
from cave import Cave
import game_world








def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            hunter.handle_event(event)


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
    game_world.add_object(cave, 0)
    game_world.add_objects(team, 1)
    game_world.add_object(hunter, 1)



# finalization code
def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()


def pause():
    pass

def resume():
    pass

