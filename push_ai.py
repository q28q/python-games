import time
import copy

NON = '🏼'
EMPTY = '  '
MAN = '😡'
BOX = '🔶'
GOAL = '🔹'
WALL = '🏼'
BOX_AND_GOAL = '🔷'

STOP = False

def get_map():
    return [[0, 0, 1, 1, 0],
       [1, 1, 1, 3, 1],
       [1, 5, 4, 5, 1],
       [1, 5, 3, 1, 4],
       [1, 1, 4, 3, 1],
       [0, 1, 1, 1, 0]]

MAP = get_map()

def turn(num):
    if num == 0:
        img = NON
    elif num == 1:
        img = EMPTY
    elif num == 2:
        img = MAN
    elif num == 3:
        img = BOX
    elif num == 4:
        img = GOAL
    elif num == 5:
        img = WALL
    elif num == 6:
        img = BOX_AND_GOAL

    return img

def draw(M, x, y):
    for i in M:
        for j in i:
            img = turn(j)
            print(img, end='')
        print()
    print(x, y)

X, Y = 4, 2


WIDTH = len(MAP[0])
HEIGHT = len(MAP)

history = []

def xun_copy(list_2):
    new_list = []
    for li in list_2:
        new_list.append(copy.copy(li))
    return new_list

all_maps = [[MAP, X, Y]]

class Game:
    def __init__(self, MAP, x, y, history):
        self.MAP = get_map()
        self.x = x
        self.y = y

        for key in history:
            self.move1(key)

    def if_win(self):
        res = True
        for i in self.MAP:
            for j in i:
                if j == 3:
                    res = False
                    return res
        print('win')
        return res

    def move0(self, key):
        if key == ord('d'):
            if self.x < WIDTH-1:
                self.x += 1
                return 'y'
        elif key == ord('a'):
            if self.x > 0:
                self.x += -1
                return 'y'
        elif key == ord('w'):
            if self.y > 0:
                self.y += -1
                return 'y'
        elif key == ord('s'):
            if self.y < HEIGHT-1:
                self.y += 1
                return 'y'
        return 'n'

    def move1(self, key):
        def stay():
            nonlocal key, leg
            if key == ord('a'):
                key = ord('d')
            elif key == ord('d'):
                key = ord('a')
            elif key == ord('w'):
                key = ord('s')
            elif key == ord('s'):
                key = ord('w')
            self.move0(key)
            leg = 'n'

        leg = self.move0(key)

        if self.MAP[self.y][self.x] in [0, 5]:
            stay()
        elif self.MAP[self.y][self.x] == 3:
            if key == ord('a'):
                m, n = -1, 0
            elif key == ord('d'):
                m, n = 1, 0
            elif key == ord('w'):
                m, n = 0, -1
            elif key == ord('s'):
                m, n = 0, 1

            if self.x+m < 0 or self.x+m > WIDTH-1:
                stay()
            elif self.y+n < 0 or self.y+n > HEIGHT-1:
                stay()
            elif self.MAP[self.y+n][self.x+m] in [0, 5]:
                stay()
            elif self.MAP[self.y+n][self.x+m] == 4:
                self.MAP[self.y+n][self.x+m] = 6
                self.MAP[self.y][self.x] = 1
            elif self.MAP[self.y+n][self.x+m] == 3:
                stay()
            elif self.MAP[self.y+n][self.x+m] == 6:
                stay()
            elif self.MAP[self.y+n][self.x+m] == 1:
                self.MAP[self.y+n][self.x+m], self.MAP[self.y][self.x] = 3, 1
        elif self.MAP[self.y][self.x] == 6:
            if key == ord('a'):
                m, n = -1, 0
            elif key == ord('d'):
                m, n = 1, 0
            elif key == ord('w'):
                m, n = 0, -1
            elif key == ord('s'):
                m, n = 0, 1

            if self.x+m < 0 or self.x+m > WIDTH-1:
                stay()
            elif self.y+n < 0 or self.y+n > HEIGHT-1:
                stay()
            elif self.MAP[self.y+n][self.x+m] in [0, 5]:
                stay()
            elif self.MAP[self.y+n][self.x+m] == 4:
                self.MAP[self.y+n][self.x+m] = 6
                self.MAP[self.y][self.x] = 4
            elif self.MAP[self.y+n][self.x+m] == 3:
                stay()
            elif self.MAP[self.y+n][self.x+m] == 6:
                stay()
            elif self.MAP[self.y+n][self.x+m] == 1:
                self.MAP[self.y+n][self.x+m], self.MAP[self.y][self.x] = 3, 4

        conti = True
        if [self.MAP, self.x, self.y] not in all_maps and leg == 'y':
            new_map = xun_copy(self.MAP)
            new_history = [new_map, self.x, self.y]
            all_maps.append(new_history)
            conti = False

        if self.if_win():
            return 'win', '!'

        return leg, conti

class Cell:
    def __init__(self, history): 
        self.keys = [ord('w'), ord('a'), ord('s'), ord('d')]
        self.history = history

    def try4(self):
        global STOP
        
        for key in self.keys:
            if STOP:
                break
            
            game = Game(MAP, X, Y, self.history)
            leg, conti = game.move1(key)
            #print(list(map(chr, self.history)))
            #print(chr(key), leg, conti, list(map(chr, self.history)))
            #for m in all_maps:
            #m = all_maps[-1]
            #draw(m[0], m[1], m[2])
            '''for m in all_maps:
                print(m)'''
            #input()

            if leg == 'win':
                new_history = self.history[:]
                new_history.append(key)
                history.append(new_history)
                STOP = True
            elif leg == 'y' and not conti:
                new_history = self.history[:]
                new_history.append(key)
                new_cell = Cell(new_history)
                new_cell.try4()

steps = ['s', 's', 'a', 's', 'a', 'a', 'w', 'd', 'a', 'a', 'w', 'w', 'w', 'd', 'd', 's', 's', 'd', 'd', 'w', 'w', 'a', 'w', 'a', 's', 's', 'w', 'a', 'a', 's', 's', 's', 'd', 's', 'd', 'd', 'w', 's', 'a', 'a', 'w', 'd', 'a', 'a', 'w', 'w', 'w', 'd', 'd', 's', 's', 'd', 'a', 'w', 'w', 'a', 'a', 's', 's', 's', 'd', 's', 'd', 'd', 'w', 'd', 'w', 'a', 's', 's', 'a', 'a', 'w', 'd', 'w', 'd', 'd', 's', 'a', 's', 'a', 'a', 'w', 'a', 'w', 'w', 'w', 'd', 'd', 'd', 'd', 's']

#game = Game(MAP, X, Y, [])

cell = Cell(list(map(ord, ['s', 's', 'a', 's', 'a', 'a', 'w', 'd', 'a', 'a', 'w', 'w', 'w', 'd', 'd', 's', 's', 'd', 'd', 'w', 'w', 'a', 'w', 'a', 's', 's', 'w', 'a', 'a', 's', 's', 's', 'd', 's', 'd', 'd', 'w', 's', 'a', 'a', 'w', 'd', 'a', 'a', 'w', 'w', 'w', 'd', 'd', 's', 's', 'd', 'a', 'w', 'w', 'a', 'a', 's', 's', 's', 'd', 's', 'd', 'd', 'w', 'd', 'w', 'a', 's', 's', 'a', 'a', 'w', 'd', 'w', 'd', 'd', 's'])))
start = time.time()
cell.try4()
end = time.time()

print(list(map(chr, history[0])))
print(end - start)

