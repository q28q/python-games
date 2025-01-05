import tkinter as tk

# 存储
gomoku_sites = [[0 for _ in range(15)] for _ in range(15)]
history = []
select = 0
select_adr = [0, 0]
next_g = 0

# 窗口初始化设置
window = tk.Tk()
window.title('五子棋')
window.geometry('1000x1200')
window.resizable(width=False, height=False)

# 绘制棋盘
w = tk.Canvas(window, height=1000, width=1000, bg='orange')
w.pack()

# 绘制棋盘
def draw_board():
    w.addtag_all('sb')
    w.delete('sb') # 清空画布

    for i in range(80, 980, 60):
        w.create_line(i, 80, i, 920, width=5)
        w.create_line(80, i, 920, i, width=5)
    w.create_oval(493, 493, 507, 507, fill='black')
    w.create_oval(253, 253, 267, 267, fill='black')
    w.create_oval(733, 733, 747, 747, fill='black')
    w.create_oval(733, 253, 747, 267, fill='black')
    w.create_oval(253, 733, 267, 747, fill='black')
    for i in range(15):
        w.create_text(80+60*i, 970, text=chr(97+i), font=('', 15))
        w.create_text(30, 920-60*i, text=str(i+1), font=('', 15))

def draw():
        global history, gomoku_sites
    
        draw_board()
        
        # 绘制预览光标
        if select:
            x, y = 80+60*select_adr[1], 80+60*select_adr[0]
            w.create_oval(x-25, y-25, x+25, y+25, width=3, outline='#00DEFF')

        turn = 1
        for i in history:
            x, y = 80+60*i[1], 80+60*i[0]
            if turn == 1:
                w.create_oval(x-25, y-25, x+25, y+25, fill='black')
                turn = 0
                gomoku_sites[i[0]][i[1]] = 1
            elif turn == 0:
                w.create_oval(x-25, y-25, x+25, y+25, fill='white')
                turn = 1
                gomoku_sites[i[0]][i[1]] = 2
        if history != []:
            y, x = history[-1][0], history[-1][1]
            y, x = 80+60*y, 80+60*x
            w.create_polygon(x+5, y+5, x+20, y+5, x+5, y+20,
                    outline='red', fill='red')


def callback(event):
    global select, next_g
    select = 1 # 预览修改为存在
    if event.x <= 50 or event.y <= 50:
        select = 0
        next_g = 0
        draw()
        return
    elif event.x >= 950 or event.y >= 950:
        select = 0
        next_g = 0
        draw()
        return

    def add_history():
        global gomoku_sites, history, select_adr, next_g, select

        # 将画布坐标转换为棋盘坐标
        x, y = event.x-50, event.y-50
        g_x, g_y = x//60, y//60

        if gomoku_sites[g_y][g_x] == 0:
            # 预览和落子交替
            if next_g:
                if [g_y, g_x] == select_adr:
                    history.append([g_y, g_x])
                    select = 0
                    next_g = 0
                else:
                    select_adr = [g_y, g_x]
                    next_g = 1
            else:
                select_adr = [g_y, g_x]
                next_g = 1
        return g_y, g_x

    y, x = add_history()
    draw()
    if_win(y, x)

# 悔棋
def undo():
    global select
    select = 0
    if history != []:
        y_x = history[-1]
        gomoku_sites[y_x[0]][y_x[1]] = 0

        del(history[-1])
    draw()

# 重开
def restart():
    global history, gomoku_sites, select
    select = 0
    gomoku_sites = [[0 for _ in range(15)] for _ in range(15)]
    history = []
    draw()

# 判断胜利
def if_win(y, x):
    lsts = []
    lsts.append(gomoku_sites[y]) # 横方向判断

    i = []
    for j in range(15):
        i.append(gomoku_sites[j][x])
    lsts.append(i) # 竖方向判断

    i = []
    # 计算斜线左下角坐标
    if x + y <= 14:
        start_y = x + y
        start_x = 0
    else:
        start_y = 14
        start_x = x + y - 14

    while start_y >= 0  and start_x < 15:
        i.append(gomoku_sites[start_y][start_x])
        start_y -= 1
        start_x += 1
    lsts.append(i) # 右上方向判断

    i = []
    # 计算斜线左上角坐标
    if y >= x:
        start_y = y - x
        start_x = 0
    else:
        start_y = 0
        start_x = x - y

    while start_y < 15 and start_x < 15:
        i.append(gomoku_sites[start_y][start_x])
        start_y += 1
        start_x += 1
    lsts.append(i) #右下方向判断

    def search_5(lst):
        black = 0
        white = 0
        now = 0
        for i in lst:
            if black == 5:
                return 'black'
            elif white == 5:
                return 'white'

            if i == 0:
                black = 0
                white = 0
                now = 0
            elif i == 1:
                if now == 1:
                    black += 1
                else:
                    black += 1
                    white = 0
                    now = 1
            elif i == 2:
                if now == 2:
                    white += 1
                else:
                    black = 0
                    white += 1
                    now = 2
        return 0
    
    for i in lsts:
        if search_5(i) != 0:
            print(search_5(i), 'win!')

undo = tk.Button(window, text='悔棋', command=undo)
undo.pack()
restart = tk.Button(window, text='重开', command=restart)
restart.pack()

draw_board()

# 获取鼠标输入
w.bind('<Button-1>', callback)

window.mainloop()
