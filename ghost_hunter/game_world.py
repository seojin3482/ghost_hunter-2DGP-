world= [[],[]]

def add_object(o,depth):
    world[depth].append(o)

def add_objects(ol,depth):
    world[depth]+=ol

def remove(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
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
