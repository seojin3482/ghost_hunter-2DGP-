from pico2d import *
import game_framework

# Hunter Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Hunter action Speed (frame)
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_RUN = 3
FRAMES_PER_ACTION_SLEEP=3






#1 : 이벤트 정의
RD, LD, RU, LU, TIMER,SPACE = range(6)
event_name=[]

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU
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
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

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




#3. 상태 변환 구현

next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, TIMER: SLEEP},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE},
    SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN}
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


    def add_event(self, event):
        self.event_que.insert(0, event)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)