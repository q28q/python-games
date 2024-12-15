import tkinter as tk
import tkinter.messagebox
import random

BG = '#222222'
Blk = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
TICK = 1000

root = tk.Tk()
root.title('俄罗斯方块')
root.resizable(0, 0)

cv = tk.Canvas(width=400, height=800, bg=BG)
cv.pack()

def callback(inp):
    key = inp.char
    game.control(key)

def random_block():
    cho = random.choice(Blk)
    shapes, color, x_y, num = eval('Data.'+cho)
    block = Block(shapes, color, x_y, num)
    game.blocks.append(block)

class Data:
    A = [[ [[0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]] ], '#ffd700', [3, -2], 1]

    B = [[ [[0, 0, 2, 0],
            [2, 2, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           
           [[0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 2, 0],
            [0, 0, 0, 0]],

           [[0, 0, 0, 0],
            [2, 2, 2, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0]],

           [[2, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0]] ], '#f68f46', [3, -3], 2]

    C = [[ [[3, 3, 0, 0],
            [0, 3, 3, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],

           [[0, 0, 3, 0],
            [0, 3, 3, 0],
            [0, 3, 0, 0],
            [0, 0, 0, 0]],

           [[0, 0, 0, 0],
            [3, 3, 0, 0],
            [0, 3, 3, 0],
            [0, 0, 0, 0]],

           [[0, 3, 0, 0],
            [3, 3, 0, 0],
            [3, 0, 0, 0],
            [0, 0, 0, 0]] ], '#ef4a53', [3, -3], 3]

    D = [[ [[0, 4, 4, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],

           [[0, 4, 0, 0],
            [0, 4, 4, 0],
            [0, 0, 4, 0],
            [0, 0, 0, 0]],

           [[0, 0, 0, 0],
            [0, 4, 4, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0]],

           [[4, 0, 0, 0],
            [4, 4, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 0, 0]] ], '#61bd5c', [3, -3], 4]

    E = [[ [[5, 0, 0, 0],
            [5, 5, 5, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],

           [[0, 5, 5, 0],
            [0, 5, 0, 0],
            [0, 5, 0, 0],
            [0, 0, 0, 0]],

           [[0, 0, 0, 0],
            [5, 5, 5, 0],
            [0, 0, 5, 0],
            [0, 0, 0, 0]],

           [[0, 5, 0, 0],
            [0, 5, 0, 0],
            [5, 5, 0, 0],
            [0, 0, 0, 0]] ], '#0076bd', [3, -3], 5]

    F = [[ [[0, 6, 0, 0],
            [6, 6, 6, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],

           [[0, 6, 0, 0],
            [0, 6, 6, 0],
            [0, 6, 0, 0],
            [0, 0, 0, 0]],

           [[0, 0, 0, 0],
            [6, 6, 6, 0],
            [0, 6, 0, 0],
            [0, 0, 0, 0]],

           [[0, 6, 0, 0],
            [6, 6, 0, 0],
            [0, 6, 0, 0],
            [0, 0, 0, 0]] ], '#c73080', [3, -3], 6]

    G = [[ [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [7, 7, 7, 7],
            [0, 0, 0, 0]],

           [[0, 7, 0, 0],
            [0, 7, 0, 0],
            [0, 7, 0, 0],
            [0, 7, 0, 0]],

           [[0, 0, 0, 0],
            [7, 7, 7, 7],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],

           [[0, 0, 7, 0],
            [0, 0, 7, 0],
            [0, 0, 7, 0],
            [0, 0, 7, 0]] ], '#4aa5e9', [3, -5], 7]

class Block:
    def __init__(self, shapes, color, x_y, num):
        self.shapes = shapes

        self.color = color
        self.stop = False

        self.shape = random.choice(self.shapes)

        self.x, self.y = x_y
        self.px, self.py = x_y

        self.num = num
    
    def scale(self):
        l = len(self.shapes)
        if self.shapes.index(self.shape) == 0:
            nl = l - 1
        nl = self.shapes.index(self.shape) - 1

        self.shape = self.shapes[nl]

    def unscale(self):
        l = len(self.shapes)
        nl = (self.shapes.index(self.shape) + 1) % l

        self.shape = self.shapes[nl]

    def move(self, key):
        px, py = self.x, self.y
        if key == 'a':
            px -= 1
        elif key == 'd':
            px += 1
        elif key == 's':
            py += 1
        elif key == 'w':
            self.scale()
        
        wrong = False
        stop = False
        for i in range(4):
            for j in range(4):
                x, y = px+i, py+j
                if self.shape[j][i] != 0 and (x<0 or x>9 or y>19):
                    if key == 'w':
                        self.unscale()
                    wrong = True
                    if y > 19:
                        stop = True
                    
                elif self.shape[j][i] != 0 and game.stop_blocks_map[x][y] != 0:
                    if y >= 0:
                        wrong = True
                        if key == 's':
                            stop = True

        if stop:
            self.stop = True
            game.update_block(self, game.stop_blocks_map)
            random_block()
        if wrong:
            pass
        else:
            self.x, self.y = px, py
        #self.x, self.y = self.px, self.py
        game.update()

        if game.if_end():
            game.ing = False
            tk.messagebox.showinfo('游戏结束', f'分数：{game.score}')

class Game:
    def __init__(self, cv):
        self.ing = True
        self.score = 0

        self.cv = cv
        self.map = [[0 for _ in range(20)] for _ in range(10)]
        
        self.stop_blocks_map = [[0 for _ in range(20)] for _ in range(10)]

        self.blocks = []

    def control(self, key):
        block = self.blocks[-1]
        if not block.stop:
            block.move(key)

    def update_block(self, block, map_):
            x, y = block.x, block.y
            shape = block.shape
            num = block.num
            
            for i in range(4):
                for j in range(4):
                    mx, my = x + i, y + j
                    if shape[j][i] != 0 and my >= 0:
                        map_[mx][my] = num

    def update(self):
        self.cv.delete(tk.ALL)
        
        self.destroy_line()
        for x in range(10):
            for y in range(20):
                self.map[x][y] = self.stop_blocks_map[x][y]

        
        for block in self.blocks:
            if not block.stop:
                self.update_block(block, self.map)

        self.draw()
    
    def draw(self):

        for x in range(9):
            cv.create_line(x*40+40, 0, x*40+40, 800, fill='white')
        for y in range(19):
            cv.create_line(0, y*40+40, 400, y*40+40, fill='white')

        for x in range(10):
            for y in range(20):
                if self.map[x][y] != 0:
                    if self.map[x][y] == 1:
                        color = Data.A[1]
                    elif self.map[x][y] == 2:
                        color = Data.B[1]
                    elif self.map[x][y] == 3:
                        color = Data.C[1]
                    elif self.map[x][y] == 4:
                        color = Data.D[1]
                    elif self.map[x][y] == 5:
                        color = Data.E[1]
                    elif self.map[x][y] == 6:
                        color = Data.F[1]
                    elif self.map[x][y] == 7:
                        color = Data.G[1]
                    self.cv.create_rectangle(x*40, y*40, x*40+40, y*40+40, fill=color)

    def destroy_line(self):
        for col in range(20):
            if_do = True
            for cow in range(10):
                if self.stop_blocks_map[cow][col] == 0:
                    if_do = False
            if if_do:
                for cow in range(10):
                    self.stop_blocks_map[cow][col] = 0
        cond = True
        while cond:
            n = 1
            for col in range(20):
                if_conti = False

                if_all_empty = True
                for cow in range(10):
                    if self.stop_blocks_map[cow][col] != 0:
                        if_all_empty = False
                        n = 0
                if if_all_empty and n == 0:
                    if_conti = True

            if if_conti:
                for col in range(19, 0, -1):
                    if_do = True
                    for cow in range(10):
                        if self.stop_blocks_map[cow][col] != 0:
                            if_do = False
                    if if_do:
                        for cow in range(10):
                            self.stop_blocks_map[cow][col], self.stop_blocks_map[cow][col-1] = self.stop_blocks_map[cow][col-1], self.stop_blocks_map[cow][col]
                            game.score += 10
            else:
                cond = False

    def if_end(self):
        for i in range(10):
            if self.stop_blocks_map[i][0] != 0:
                return True
        return False

    def loop(self):
        block = self.blocks[-1]
        if not block.stop:
            block.move('s')
        if self.ing:
            self.cv.after(TICK, self.loop)
        
game = Game(cv)
random_block()

game.update()
game.loop()

game.cv.bind('<Key>', callback)
game.cv.focus_set()

root.mainloop()
