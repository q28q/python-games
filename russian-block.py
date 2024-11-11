import threading
import curses
import time
import random

def main(x):
    
    # 初始化窗口
    global block
    global scr
    global lock
    global error
    global cond
    global scr2
    global scr3
    global score
    global next
    score = 0
    cond = True
    lock = threading.Lock()
    scr = curses.newwin(height+2, width*2+2, 0, 0)
    scr.keypad(1)
    curses.curs_set(0)
    scr.border()
    
    scr.refresh()
    
    scr2 = curses.newwin(int(height/4)+2, width*2+2, 0, width*2+4)
    scr2.border()
    scr2.refresh()
    draw2()
    
    scr3 = curses.newwin(height-int(height/4), width*2+2, int(height/4)+2, width*2+4)
    scr3.border()
    scr3.refresh()
    draw3(next_2[1], next_2_type[1])
    
    # 生成新方块
    block = Block(next_2[0])
    
  # 新建更新游戏线程
    t = threading.Thread(target=refresh, args=[])
    t.start()
    
    # 控制部分
    last_time = time.time()
    while cond:
        try:
            a = scr.getch()
            block.move(a)
            put(block.site)
            draw()
        except KeyboardInterrupt:
            cond = False
            t.join()
            return
        except Exception as err:
            error = err
            cond = False
            t.join()
            return
    
# 返回最值
def most_yx(site):
    left_x = width
    right_x = 0
    down_y = 0
    for i in site:
        if i[0] > down_y:
            down_y = i[0]
        if i[1] > right_x:
            right_x = i[1]
        if i[1] < left_x:
            left_x = i[1]
            
    return down_y, left_x, right_x
    
def draw2():
    lock.acquire()
    global scr2
    scr2.addstr(int(height/8)+1, 1, '分数：')
    scr2.addstr(int(height/8)+1, 7, str(score))
    scr2.refresh()
    lock.release()
   
def draw3(name, type_):
    lock.acquire()
    global scr3
    global next
    scr3.erase()
    scr3.border()
    scr3.addstr(1, 1, '下一个：')
    y = int((height-int(height/4))/2)-1
    x = width
    O = [[0, 0], [0, 1], [1, 0], [1, 1]]
    T1 = [[0, 0], [0, 1], [0, -1], [1, 0]]
    T2 = [[0, 0], [-1, 0], [1, 0], [0, -1]]
    T3 = [[0, 0], [0, -1], [0, 1], [-1, 0]]
    T4 = [[0, 0], [0, 1], [1, 0], [-1, 0]]
    I1 = [[0, 0], [1, 0], [2, 0], [-1, 0]]
    I2 = [[0, 0], [0, 1], [0, 2], [0, -1]]
    S1 = [[0, 0], [0, 1], [1, 0], [1, -1]]
    S2 = [[0, 0], [-1, 0], [0, 1], [1, 1]]
    Z1 = [[0, 0], [0, -1], [1, 0], [1, 1]]
    Z2 = [[0, 0], [0, 1], [-1, 1], [1, 0]]
    J1 = [[0, 0], [-1, 0], [1, 0], [1, -1]]
    J2 = [[0, 0], [0, 1], [0, -1], [-1, -1]]
    J3 = [[0, 0], [1, 0], [-1, 0], [-1, 1]]
    J4 = [[0, 0], [0, -1], [0, 1], [1, 1]]
    L1 = [[0, 0], [-1, 0], [1, 0], [1, 1]]
    L2 = [[0, 0], [0, 1], [0, -1], [1, -1]]
    L3 = [[0, 0], [1, 0], [-1, 0], [-1, -1]]
    L4 = [[0, 0], [0, -1], [0, 1], [1, 1]]
    
    if name == 'O':
        for i in O:
            scr3.addstr(y+i[0], x+(i[1])*2, chicken)
    if name == 'T':
        if type_ == 1:
            for i in T1:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 2:
            for i in T2:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 3:
            for i in T3:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 4:
            for i in T4:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
    if name == 'I':
        if type_ == 1 or type_ == 3:
            for i in I1:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 2 or type_ == 4:
            for i in I2:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
    if name == 'S':
        if type_ == 1 or type_ == 3:
            for i in S1:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 2 or type_ == 4:
            for i in S2:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
    if name == 'Z':
        if type_ == 1 or type_ == 3:
            for i in Z1:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 2 or type_ == 4:
            for i in Z2:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
    if name == 'J':
        if type_ == 1:
            for i in J1:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 2:
            for i in J2:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 3:
            for i in J3:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 4:
            for i in J4:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
    if name == 'L':
        if type_ == 1:
            for i in L1:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 2:
            for i in L2:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 3:
            for i in L3:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
        if type_ == 4:
            for i in L4:
                scr3.addstr(y+i[0], x+(i[1])*2, chicken)
    scr3.refresh()
    lock.release()

# 清除map_里所有的1
def clean1():
    for i in range(4, height+4):
        for j in range(width):
            if map_[i][j] == 1:
                map_[i][j] = 0
                
# 把map_里所有的1改为2
def change1_2():
    for i in range(4, height+4):
        for j in range(width):
            if map_[i][j] == 1:
                map_[i][j] = 2
                
# 把各方块坐标放入map_中
def put(x):
    clean1()
       
    for i in x:
        map_[i[0]][i[1]] = 1
                
# 根据map_列表输出画面
def draw():
    lock.acquire()
    for i in range(4, height+4):
        for j in range(width):
            if map_[i][j] == 0:
                scr.addstr(i-3, j*2+1, background)
            elif map_[i][j] == 1:
                scr.addstr(i-3, j*2+1, chicken)
            elif map_[i][j] == 2:
                scr.addstr(i-3, j*2+1, meat)
    scr.refresh()
    lock.release()
    
# 判断游戏是否失败
def if_lose():
    global cond
    for i in range(width):
        if map_[4][i] == 2:
            cond = 0
            return 1
    return 0

def remove_line():
    global score
    n = 0
    k = 0
    for i in range(4, height+4):
        if sum(map_[i]) == width*2:
            if k == 0:
                k = i
            n += 1
            for j in range(width):
                map_[i][j] = 0
    score += n*width
    draw2()
    down(n, k)
                
def down(x, y):
    for i in range(y, 3, -1):
        for j in range(width):
            if map_[i][j] == 2:
                 map_[i][j] = 0
                 map_[i+x][j] = 2
                 
def remove_same(dir_):
    
    A = []
    for i in dir_:
        if i not in A:
            A.append(i)
    return A
    
# 更新游戏
def refresh():
    global cond
    global block
    while cond:
        if if_lose():
            break
        remove_line()
        #draw3(next_2[1], next_2_type[1])
                
        a = block.update()
        if a == 0:
            next_2.remove(next_2[0])
            next_2.append(random.choice(blocks))
            next_2_type.remove(next_2_type[0])
            next_2_type.append(random.randint(1, 4))
            draw3(next_2[1], next_2_type[1])
            block = Block(next_2[0])
            block.move(curses.KEY_DOWN)
          
        time.sleep(0.3)
        
           
class Block:
    def __init__(self, name):
        self.name = name
        self.type_ = next_2_type[0]
        self.x = int((width-1)/2)
        self.y = 2
        self.valid = True
        self.generate()        
        self.most_site = 0
        most_d = []
        for i in self.site:
            most_d.append(i[0])
        most_d = max(most_d)
        self.y -= most_d - 2
        
    # 生成各方块坐标
    def generate(self):
        if self.name == 'O':
            self.n1 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y+1, self.x], [self.y+1, self.x+1]]
            self.n2 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y+1, self.x], [self.y+1, self.x+1]]
            self.n3 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y+1, self.x], [self.y+1, self.x+1]]
            self.n4 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y+1, self.x], [self.y+1, self.x+1]]
            
            if self.type_ == 1:
                self.site = self.n1
            elif self.type_ == 2:
                self.site = self.n2
            elif self.type_ == 3:
                self.site = self.n3
            elif self.type_ == 4:
                self.site = self.n4
        elif self.name == 'T':
            self.n1 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y, self.x-1], [self.y+1, self.x]]
            self.n2 = [[self.y, self.x], [self.y, self.x-1]
            , [self.y-1, self.x], [self.y+1, self.x]]
            self.n3 = [[self.y, self.x], [self.y-1, self.x]
            , [self.y, self.x-1], [self.y, self.x+1]]
            self.n4 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y-1, self.x], [self.y+1, self.x]]

            if self.type_ == 1:
                self.site = self.n1
            elif self.type_ == 2:
                self.site = self.n2
            elif self.type_ == 3:
                self.site = self.n3
            elif self.type_ == 4:
                self.site = self.n4
        elif self.name == 'I':
            self.n1 = [[self.y, self.x], [self.y+1, self.x]
            , [self.y+2, self.x], [self.y-1, self.x]]
            self.n2 = [[self.y, self.x+1], [self.y, self.x+2]
            , [self.y, self.x], [self.y, self.x-1]]
            self.n3 = [[self.y+1, self.x+1], [self.y+2, self.x+1]
            , [self.y, self.x+1], [self.y-1, self.x+1]]
            self.n4 = [[self.y+1, self.x], [self.y+1, self.x-1]
            , [self.y+1, self.x+1], [self.y+1, self.x+2]]
    
            if self.type_ == 1:
                self.site = self.n1
            elif self.type_ == 2:
                self.site = self.n2
            elif self.type_ == 3:
                self.site = self.n3
            elif self.type_ == 4:
                self.site = self.n4
        elif self.name == 'S':
            self.n1 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y+1, self.x], [self.y+1, self.x-1]]
            self.n2 = [[self.y, self.x], [self.y+1, self.x]
            , [self.y, self.x-1], [self.y-1, self.x-1]]
            self.n3 = [[self.y, self.x], [self.y-1, self.x]
            , [self.y, self.x-1], [self.y-1, self.x+1]]
            self.n4 = [[self.y, self.x], [self.y-1, self.x]
            , [self.y, self.x+1], [self.y+1, self.x+1]]

            if self.type_ == 1:
                self.site = self.n1
            elif self.type_ == 2:
                self.site = self.n2
            elif self.type_ == 3:
                self.site = self.n3
            elif self.type_ == 4:
                self.site = self.n4
        elif self.name == 'Z':
            self.n1 = [[self.y, self.x], [self.y, self.x-1]
            , [self.y+1, self.x], [self.y+1, self.x+1]]
            self.n2 = [[self.y, self.x], [self.y-1, self.x]
            , [self.y, self.x-1], [self.y+1, self.x-1]]
            self.n3 = [[self.y, self.x], [self.y-1, self.x]
            , [self.y-1, self.x-1], [self.y, self.x+1]]
            self.n4 = [[self.y, self.x], [self.y+1, self.x]
            , [self.y, self.x+1], [self.y-1, self.x+1]]

            if self.type_ == 1:
                self.site = self.n1
            elif self.type_ == 2:
               self.site = self.n2
            elif self.type_ == 3:
                self.site = self.n3
            elif self.type_ == 4:
                self.site = self.n4
        elif self.name == 'L':
            self.n1 = [[self.y, self.x], [self.y+1, self.x]
            , [self.y+1, self.x+1], [self.y-1, self.x]]
            self.n2 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y, self.x-1], [self.y+1, self.x-1]]
            self.n3 = [[self.y, self.x], [self.y-1, self.x]
            , [self.y-1, self.x-1], [self.y+1, self.x]]
            self.n4 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y-1, self.x+1], [self.y, self.x-1]]
    
            if self.type_ == 1:
               self.site = self.n1
            elif self.type_ == 2:
                self.site = self.n2
            elif self.type_ == 3:
                self.site = self.n3
            elif self.type_ == 4:
                self.site = self.n4
        elif self.name == 'J':
            self.n1 = [[self.y, self.x], [self.y-1, self.x]
            , [self.y+1, self.x], [self.y+1, self.x-1]]
            self.n2 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y, self.x-1], [self.y-1, self.x-1]]
            self.n3 = [[self.y, self.x], [self.y+1, self.x]
            , [self.y-1, self.x], [self.y-1, self.x+1]]
            self.n4 = [[self.y, self.x], [self.y, self.x+1]
            , [self.y, self.x-1], [self.y+1, self.x+1]]

            if self.type_ == 1:
                self.site = self.n1
            elif self.type_ == 2:
                self.site = self.n2
            elif self.type_ == 3:
                self.site = self.n3
            elif self.type_ == 4:
                self.site = self.n4
            
    def don_rotate(self):
        if self.type_ == 1:
            for i in self.n2:
                if i[1] > width - 1:
                    return 0
                elif i[1] < 0:
                    return 0
                elif i[0] > height + 3:
                    return 0
                elif map_[i[0]][i[1]] == 2:
                    return 0
        elif self.type_ == 2:
            for i in self.n3:
                if i[1] > width - 1:
                    return 0
                elif i[1] < 0:
                    return 0
                elif i[0] > height +3:
                    return 0
                elif map_[i[0]][i[1]] == 2:
                    return 0
        elif self.type_ == 3:
            for i in self.n4:
                if i[1] > width - 1:
                    return 0
                elif i[1] < 0:
                    return 0
                elif i[0] > height + 3:
                    return 0
                elif map_[i[0]][i[1]] == 2:
                    return 0
        elif self.type_ == 4:
            for i in self.n1:
                if i[1] > width - 1:
                    return 0
                elif i[1] < 0:
                    return 0
                elif i[0] > height + 3:
                    return 0
                elif map_[i[0]][i[1]] == 2:
                    return 0
        return 1
    
    # 获取极坐标
    def kick_wall(self, direct):
        self.most_site = most_yx(self.site)
        return self.most_site
        
    def no_to_2(self):
        self.kick_wall(self.site)
        dir_x = []
        dir_y = []
        for i in self.site:
            dir_y.append(i[0])
            dir_x.append(i[1])
        dir_x = remove_same(dir_x)
        dir_y = remove_same(dir_y)
        
        # 得到每行每列的坐标
        y_lines = []
        for i in dir_x:
            y_line = []
            for j in self.site:
                if j[1] == i:
                    y_line.append(j)
            y_lines.append(y_line)
        x_lines = []
        for i in dir_y:
            x_line = []
            for j in self.site:
                if j[0] == i:
                    x_line.append(j)
            x_lines.append(x_line)
        
        d = 1
        l = 1
        r = 1
        
        # 下方有鸡肉时禁止向下运动
        for i in range(len(y_lines)):
            most_d = [0, 0]
            for j in range(len(y_lines[i])):
                if y_lines[i][j][0] > most_d[0]:
                    most_d = y_lines[i][j]
            try:
                if map_[most_d[0]+1][most_d[1]] == 2:
                    d = 0
            except:
                d = 0
        # 旁边有鸡肉时禁止向旁边运动
        for i in range(len(x_lines)):
            most_l = [0, width]
            most_r = [0, 0]
            for j in range(len(x_lines[i])):
                if x_lines[i][j][1] < most_l[1]:
                    most_l = x_lines[i][j]
                if x_lines[i][j][1] > most_r[1]:
                    most_r = x_lines[i][j]
            try:
                if map_[most_l[0]][most_l[1]-1] == 2:
                    l = 0
            except:
                l = 0
            try:
                if map_[most_r[0]][most_r[1]+1] == 2:
                    r = 0
            except:
                r = 0
              
        return d, l, r
         
    # 方块掉落
    def update(self):
        global block
        ret = None
        self.kick_wall(self.site)
        if self.most_site[0] == height+3:
            change1_2()
            #block = O()
            self.valid = False
            ret = 0
           
        elif self.no_to_2()[0] != 0:
            self.y += 1
            self.generate()
            put(self.site)
            
        elif self.no_to_2()[0] == 0:
            change1_2()
            #block = O()
            self.valid = False
            ret = 0
        
        draw()
        return ret
         
            
    # 控制函数
    def move(self, a):
        global block
            
        # 获取键盘输入并返回变化量
        self.kick_wall(self.site)
        _x = 0
        _y = 0
        if a == curses.KEY_RIGHT and self.most_site[2] < width-1 and self.no_to_2()[2] == 1:
            _x = 1
        elif a == curses.KEY_LEFT and self.most_site[1] > 0 and self.no_to_2()[1] == 1:
            _x = -1
        elif a == curses.KEY_DOWN and self.most_site[0] < height+3 and self.no_to_2()[0] == 1 and self.most_site[0] != height+3:
            _y = 1
        elif a == curses.KEY_UP and self.don_rotate():
            self.rotate()
        elif a == -1:
            pass

        if not self.valid:
            self = block
            
        # 根据变化量改变关键块位置
        self.y += _y
        self.x += _x
            
        # 重新生成各块位置
        self.generate()
        put(self.site)
        
    def rotate(self):
        self.type_ = self.type_ + 1
        if self.type_ > 4:
            self.type_ = 1
        self.generate() 
                                  
height = 20
width = 10
chicken = '🔲'
meat = '🔳'
background = '  '

error = None
    
map_ = [[0 for _ in range(width)] for _ in range(height+4)]
blocks = ['O', 'T', 'I', 'S', 'Z', 'J', 'L']
next_2 = random.choices(blocks, k=2)
next_2_type = [random.randint(1, 4), random.randint(1, 4)]
   
curses.wrapper(main)
if error != None:
    import traceback
    traceback.print_exception(error)
print(score)
