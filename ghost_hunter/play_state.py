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
team=None #ghost list


# 초기화
def enter():
    global cave,hunter,team,running
    team=[Ghost()for i in range(1)] #ghost number 지정
    hunter=Hunter()
    cave=Cave()
    running = True
    game_world.add_object(cave, 0)
    game_world.add_objects(team, 1)
    game_world.add_object(hunter, 1)


    #충돌 리스트 추가
    game_world.add_collision_pairs(hunter, team, 'hunter:team')



# finalization code
def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('COLLISION ', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)







    # for ghost in team:
    #     if collide(hunter,ghost):
    #         print('collision')




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

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True
