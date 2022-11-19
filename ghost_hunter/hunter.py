from pico2d import *
import game_framework
import game_world

# Hunter Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Hunter action Speed (frame)
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_RUN = 3
FRAMES_PER_ACTION_SLEEP=3






#1 : 이벤트 정의
RD, LD, RU, LU, TIMER,SPACE,AD,AU,SD,SU,COLLIDE= range(11)
event_name=[]

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN,SDLK_a):AD,
    (SDL_KEYUP,SDLK_a):AU,
    (SDL_KEYDOWN, SDLK_s): SD,
    (SDL_KEYUP, SDLK_s): SU
}


#2 : 상태의 정의
class IDLE:
    @staticmethod
    def enter(self,event):
        print('ENTER IDLE')
        self.dir = 0
        self.timer = 10000

    @staticmethod
    def exit(self,event):
        print('EXIT IDLE')



    @staticmethod
    def do(self):
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)


    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(0, 565, 113, 133, -3.141592, 'v', self.x, self.y, 113, 113)
        else:
            self.image.clip_draw(0, 565, 113, 133, self.x, self.y, 113, 113)


class RUN:
    def enter(self, event):
        print('ENTER RUN')
        if event == RD:
            self.dir = 1
        elif event == LD:
            self.dir = -1
        # elif event == RU:
        #     self.dir -= 1
        # elif event == LU:
        #     self.dir += 1

    def exit(self,event):
        print('EXIT RUN')
        self.face_dir = self.dir


    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 3+6
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time #방향*속도*시간
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 113, 569, 113, 113, self.x, self.y)

        elif self.dir == -1:
            self.image.clip_composite_draw(int(self.frame) * 113, 569, 113, 133, -3.141592, 'v', self.x, self.y, 113, 113)



class SLEEP:

    def enter(self, event):
        print('ENTER SLEEP')
        self.frame = 0

    def exit(self,event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_SLEEP * ACTION_PER_TIME * game_framework.frame_time) % 3+6 #6,7,8

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(int(self.frame) * 113, 113, 113, 113,
                                          0, '', self.x + 25, self.y+10 , 113, 113)
        else:
            self.image.clip_composite_draw(int(self.frame) * 113, 113, 113, 113,
                                          -3.141592, 'v', self.x - 25, self.y+10, 113, 113)




class ATTACK:
    def enter(self, event):
        print('ENTER ATTACK')


    def exit(self,event):
        print('EXIT RUN')



    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 3+3
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.face_dir == -1 or self.dir==-1:
            self.image.clip_draw(int(self.frame) * 113, 113*5, 113, 113, self.x, self.y)

        elif self.face_dir == 1 or self.dir==1:
            self.image.clip_composite_draw(int(self.frame) * 113, 113*5, 113, 133, -3.141592, 'v', self.x, self.y, 113, 113)


class DAMAGE:

    def enter(self, event):
        print('ENTER DAMAGE')


    def exit(self,event):
            print('EXIT RUN')



    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x = clamp(0, self.x, 800)



    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(int(self.frame) * 113, 113, 113, 113, self.x+40, self.y)

        elif self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 113, 113, 113, 113, -3.141592, 'v', self.x-40, self.y, 113, 113)


#점프 수정
class JUMP:
        def enter(self, event):
            print('ENTER JUMP')
            # if event == RD:
            #     self.dir = 1
            # elif event == LD:
            #     self.dir = -1
            # # elif event == RU:
            # #     self.dir -= 1
            # # elif event == LU:
            # #     self.dir += 1
            self.v = 5 # 속도
            self.m = 5  # 질량

        def exit(self, event):
            print('EXIT JUMP')


        def do(self):
            #run 상태와 동일한 프레임 적용
            self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 3 + 6
            # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
            if self.v > 0:
                # 속도가 0보다 클때는 위로 올라감
                F = (0.5 * self.m * (self.v * self.v))
            else:
                # 속도가 0보다 작을때는 아래로 내려감
                F = -(0.5 * self.m * (self.v * self.v))

            # 좌표 수정 : 위로 올라가기 위해서는 y 좌표를 줄여준다.
            self.y -= round(F)

            # 속도 줄여줌
            self.v -= 1

            # # 바닥에 닿았을때, 변수 리셋
            # if self.y-50 > 160:
            #     #self.y-50 = 160
            #
            #     self.v = 10.0




        def draw(self):
            if self.dir == 1 or self.face_dir==1:
                self.image.clip_draw(int(self.frame) * 113, 569, 113, 113, self.x, self.y)

            elif self.dir == -1 or self.face_dir==-1:
                self.image.clip_composite_draw(int(self.frame) * 113, 569, 113, 133, -3.141592, 'v', self.x, self.y,
                                               113, 113)


#3. 상태 변환 구현

next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, TIMER: SLEEP,AD:ATTACK,AU:ATTACK,SD:JUMP,SU:JUMP,COLLIDE:DAMAGE},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE,AD:ATTACK,AU:ATTACK,SD:JUMP,SU:JUMP,COLLIDE:DAMAGE},
    SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN,AD:ATTACK,AU:ATTACK,SD:JUMP,SU:JUMP,COLLIDE:DAMAGE},


    ATTACK: {RU: RUN, LU: RUN, RD: RUN, LD: RUN,AD:IDLE,AU:IDLE,SD:JUMP,SU:JUMP,COLLIDE:DAMAGE},
    DAMAGE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN,SD:JUMP,SU:JUMP,AD:ATTACK,AU:ATTACK,COLLIDE:DAMAGE},
    JUMP:{RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, TIMER: SLEEP,AD:ATTACK,AU:ATTACK,SD:IDLE,SU:IDLE,COLLIDE:DAMAGE}

}



class Hunter:
    def __init__(self):
        self.x, self.y = 400, 160
        self.frame = 0
        self.frame2 =0
        self.dir = 0  # 오른쪽
        self.face_dir=1
        self.image = load_image('hunter.png')

        self.timer=1000

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)

            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__} Event {event_name[event]}')

            self.cur_state.enter(self, event)



    def draw(self):
        self.cur_state.draw(self)
        debug_print('PPPP')
        debug_print(f'Face Dir: {self.face_dir}, Dir: {self.dir}')
        draw_rectangle(*self.get_bb())


    def add_event(self, event):
        self.event_que.insert(0, event)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb(self):
        if self.cur_state==ATTACK:
            if self.face_dir==1:
                return self.x+10,self.y-20,self.x+40,self.y+40
            elif self.face_dir == -1:
                return self.x-40,self.y-20,self.x-10,self.y+40

        elif self.cur_state==DAMAGE:
            if self.face_dir==1 or self.dir==1:
                return self.x-55,self.y-50,self.x-25,self.y+50
            elif self.face_dir == -1 or self.face_dir==-1:
                return self.x+25,self.y-50,self.x+55,self.y+50

        else:
            return self.x - 15, self.y - 50, self.x + 15, self.y + 50

    def handle_collision(self, other, group):
        if group == 'hunter:team':
            self.add_event(COLLIDE)

        #     #hunter의 hp 감소
        #     #hunter 데미지 입었을 때


