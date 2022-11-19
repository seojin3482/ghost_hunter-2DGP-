world= [[],[]] #list of list


#충돌 딕셔너리
collision_group=dict()
#딕셔너리 형태
# key -> hunter:team 어떤 객체끼리의 충돌인지 string 정보
# value -> [ [hunter],[ghost1,ghost2,ghost3] ] list of list


def add_object(o,depth):
    world[depth].append(o)

def add_objects(ol,depth):
    world[depth]+=ol

def remove(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return

def all_objects(): #낮은거 부터 나옴.. 모든 객체를 하나씩 꺼내서 던져주는 역할
    for layer in world:
        for o in layer:
            yield o
def clear():
    for o in all_objects():
        del o
    for layer in world:
        layer.clear()


def add_collision_pairs(a, b, group):
    if group not in collision_group:
        print('Add new group ', group)
        collision_group[group] = [ [], [] ] # list of list : list pair
        if b:
            if type(b) is list:
                collision_group[group][1] += b
            else:
                collision_group[group][1].append(b)
        if a:
            if type(a) is list:
                collision_group[group][0] += a
            else:
                collision_group[group][0].append(a)

def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
