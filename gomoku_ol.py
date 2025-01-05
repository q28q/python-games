import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import random

IP = '192.168.125.131'

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x700')
        self.root.title('五子棋')
        self.root.configure(bg='#f8f8ff')
        self.root.columnconfigure(0, weight=1)

        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.history = []
        self.name_i = 'my_name'
        self.name_u = 'your_name'
        self.type = 'single'
        self.sock = 'server'
        self.color = 'black'

        self.board_cv = tk.Canvas(width=500, height=500, bg='#ffcc00')
        self.leave = tk.Button(font=('仿宋', 20), text='退出', command=self.draw_main)

        self.make = tk.Button(text='创建房间', font=('仿宋', 24), bg='orange')
        self.make.configure(activebackground='#ff7f00')
        self.make.configure(command=lambda: (self.draw_make_room(), self.sure.configure(command=self.open_game)))
        self.add = tk.Button(text='加入游戏', font=('仿宋', 24), bg='orange')
        self.add.configure(activebackground='#ff7f00')
        self.add.configure(command=lambda: (self.draw_make_room(), self.sure.configure(command=self.add_game)))
        
        self.single = tk.Button(text='本地对战', font=('仿宋', 24), bg='orange')
        self.single.configure(activebackground='#ff7f00')
        self.single.configure(command=lambda: (self.clear_single_game(), self.draw_single_game()))

        self.double = tk.Button(text='联机对战', font=('仿宋', 24), bg='orange')
        self.double.configure(activebackground='#ff7f00')
        self.double.configure(command=self.draw_choose)

        self.undo = tk.Button(text='悔棋', font=('仿宋', 20))
        self.undo.configure(command=self.back)

        self.room_num = tk.Entry(font=('仿宋', 24), bg='yellow')
        self.sure = tk.Button(font=('仿宋', 24), text='确定', bg='orange')
        self.sure.configure(activebackground='#ff7f00')
        self.leave_to_choose = tk.Button(font=('仿宋', 20), text='退出')
        self.leave_to_choose.configure(command=self.draw_choose)
        self.get_name = tk.Entry(font=('仿宋', 24), bg='yellow')
        self.label_room = tk.Label(text='请输入房间号', bg='#f8f8ff')
        self.label_room.configure(font=('宋体', 20))
        self.label_name = tk.Label(text='请输入名称', bg='#f8f8ff')
        self.label_name.configure(font=('宋体', 20))

        self.label_wait_o = tk.Label(text='等待连接中...')
        self.label_wait_o.configure(font=('宋体', 26), bg='#f8f8ff')
        self.label_wait_a = tk.Label(text='正在连接中...')
        self.label_wait_a.configure(font=('宋体', 26), bg='#f8f8ff')
        self.cancel = tk.Button(text='取消', bg='orange', activebackground='#ff7f00')
        self.cancel.configure(font='仿宋, 24', command=self.draw_make_room)

        self.chat_box = scrolledtext.ScrolledText(font=('', 18), bg='#F0F0F0')
        self.chat_box.configure(state='disabled')
        self.input_box = tk.Entry(font=('', 18))
        self.send_button = tk.Button(text='发送', font=('', 16))
        self.send_button.configure(command=self.send_message)
        self.multi_back = tk.Button(text='悔棋', font=('', 16))
        self.multi_back.configure(command=self.multiplayer_back)
        self.multi_leave = tk.Button(text='离开', font=('', 16), command=self.draw_main)

        self.label_i = tk.Label(text='轮到你下棋', font=('', 16))
        self.label_u = tk.Label(text='轮到对方下棋', font=('', 16))
        
    def clear_all(self):
        for i in self.root.grid_slaves():
            i.grid_forget()
        for i in self.root.place_slaves():
            i.place_forget()

    def clear_single_game(self):
        self.history = []
        self.put_history()

        self.type = 'single'

    def clear_multi_game(self):
        self.history = []
        self.put_history()

        self.type = 'double'

        self.chat_box.configure(state='normal')
        self.chat_box.delete(1.0, tk.END)
        self.chat_box.configure(state='disabled')

        self.input_box.delete(0, tk.END)

    def put_history(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        if self.history != []:
            for i in self.history:
                x, y, t = i
                self.board[x][y] = t

    def draw_main(self):
        self.clear_all()

        self.single.grid(row=0, column=0, ipadx=30, sticky='n', pady=180)

        self.double.grid(row=1, column=0, ipadx=30) 
    
    def draw_board(self):
        self.clear_all()

        self.board_cv.grid(row=0)
        
        self.board_cv.delete(tk.ALL)

        for i in range(15):
            x = 40 + i*30
            self.board_cv.create_line(x, 40, x, 460)
        for i in range(15):
            y = 40 + i*30
            self.board_cv.create_line(40, y, 460, y)
        self.board_cv.create_oval(248, 248, 252, 252, fill='black')
        self.board_cv.create_oval(128, 128, 132, 132, fill='black')
        self.board_cv.create_oval(368, 128, 372, 132, fill='black')
        self.board_cv.create_oval(128, 368, 132, 372, fill='black')
        self.board_cv.create_oval(368, 368, 372, 372, fill='black')

        for x in range(15):
            for y in range(15):
                if self.board[x][y] == 1:
                    rx, ry = map(lambda x: x*30+40, (x, y))
                    self.board_cv.create_oval(rx-14, ry-14, rx+14, ry+14, fill='#000000')
                elif self.board[x][y] == 2:
                    rx, ry = map(lambda x: x*30+40, (x, y))
                    self.board_cv.create_oval(rx-14, ry-14, rx+14, ry+14, fill='#ffffff')

        if self.history != []:
            x, y = self.history[-1][:2]
            px, py = map(lambda x: x*30+40, (x, y))
            self.board_cv.create_polygon(px, py, px+12, py, px, py+12, outline='red', fill='red')

    def draw_choose(self):
        self.clear_all()
        
        self.make.grid(row=0, column=0, ipadx=30, sticky='n', pady=180)
        self.add.grid(row=1, column=0, ipadx=30)
        self.leave.grid(row=2, sticky='w', pady=100)

    def draw_make_room(self):
        self.clear_all()

        self.label_room.place(x=250, y=120, anchor='center')
        self.label_name.place(x=250, y=310, anchor='center')
        self.room_num.grid(row=1, pady=150, ipadx=30)
        self.room_num.delete(0, 'end')
        self.get_name.grid(row=2, ipadx=30)
        self.get_name.delete(0, 'end')
        self.sure.grid(row=3, sticky='n', ipadx=30, pady=72)
        self.leave_to_choose.grid(row=4, sticky='w')

    def draw_wait_o(self):
        self.clear_all()

        self.label_wait_o.place(relx=0.5, rely=0.35, anchor='center')
        self.cancel.place(relx=0.5, rely=0.5, anchor='center', width=200)

    def draw_wait_a(self):
        self.clear_all()

        self.label_wait_a.place(relx=0.5, rely=0.35, anchor='center')
        self.cancel.place(relx=0.5, rely=0.5, anchor='center', width=200)

    def draw_single_game(self):
        self.clear_all()

        self.draw_board()

        self.leave.grid(row=1, sticky='w', pady=70)
        self.undo.grid(row=1, sticky='e')

    def draw_multiplayer(self):
        self.clear_all()

        self.draw_board()

        self.chat_box.place(x=0, y=540, width=500, height=120)
        self.input_box.place(x=0, y=660, width=430, height=40)
        self.send_button.place(x=430, y=660, width=70, height=40)
        self.multi_back.place(x=430, y=500, width=70, height=40)
        self.multi_leave.place(x=0, y=500, width=70, height=40)

        if self.color == 'black':
            if len(self.history) % 2 == 0:
                self.label_i.place(x=250, y=520, anchor='center')
            else:
                self.label_u.place(x=250, y=520, anchor='center')
        else:
            if len(self.history) % 2 == 1:
                self.label_i.place(x=250, y=520, anchor='center')
            else:
                self.label_u.place(x=250, y=520, anchor='center')
        
    def set_chess(self, event):
        x, y = event.x, event.y
        if x < 25  or x > 475:
            return
        elif y < 25 or y > 475:
            return
        g_x, g_y = map(lambda x:(x-25)//30, (x,y))

        if self.type == 'single':
            if self.board[g_x][g_y] == 0:
                if len(self.history) % 2 == 0:
                    self.history.append([g_x, g_y, 1])
                else:
                    self.history.append([g_x, g_y, 2])
                self.put_history()
                self.draw_single_game()
        else:
            if self.board[g_x][g_y] == 0:
                if self.color == 'black':
                    if len(self.history) % 2 == 0:
                        self.history.append([g_x, g_y, 1])
                        client.send(('<chess>'+str([g_x, g_y, 1])).encode('utf-8'))
                else:
                    if len(self.history) % 2 == 1:
                        self.history.append([g_x, g_y, 2])
                        client.send(('<chess>'+str([g_x, g_y, 2])).encode('utf-8'))

                self.put_history()
                self.draw_multiplayer()
            
    def back(self):
        if self.history != []:
            del(self.history[-1])
            self.put_history()
            if self.type == 'single':
                self.draw_single_game()
            else:
                self.draw_multiplayer()

    def multiplayer_back(self):
        if self.color == 'black':
            if len(self.history) % 2 == 1:
                client.send('<back_>ask'.encode('utf-8'))
        else:
            if len(self.history) % 2 == 0 and len(self.history) != 0:
                client.send('<back_>ask'.encode('utf-8'))

    def receiver(self):
        global cond

        cond = 1
        while cond:
            try:
                message = client.recv(1024).decode('utf-8')

                msg_type = message[:7]
                data = message[7:]

                if msg_type == '<chat_>':
                    self.chat_box.configure(state='normal')
                    self.chat_box.insert(tk.END, '<'+self.name_u+'>'+':'+data+'\n')
                    self.chat_box.configure(state='disabled')
                    self.chat_box.see(tk.END)
                elif msg_type == '<chess>':
                    self.history.append(eval(data))
                    self.put_history()
                    self.draw_multiplayer()
                elif msg_type == '<back_>':
                    if data == 'ask':
                        result = self.askyesno_plus('对方请求悔棋', '是否同意悔棋?', self.root)
                        if result:
                            client.send('<back_>yes'.encode('utf-8'))
                            self.back()
                        else:
                            client.send('<back_>no'.encode('utf-8'))
                    elif data == 'no':
                        self.showinfo_plus('', '对方拒绝悔棋', self.root)
                    elif data == 'yes':
                        self.back()
                    
            except ConnectionResetError:
                cond = 0
                self.draw_main()

    def server(self, port):
        global server, client
        
        host = IP
        port = int(port)
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        client, addr = server.accept()
        print('连接成功')

        self.name_u = client.recv(1024).decode('utf-8')
        client.send(self.name_i.encode('utf-8'))

        self.color = random.choice(['black', 'white'])
        if self.color == 'black':
            client.send('white'.encode('utf-8'))
        else:
            client.send('black'.encode('utf-8'))
        print(self.name_u, self.color)

        receive_line = threading.Thread(target=self.receiver)
        receive_line.start()

        self.clear_multi_game()
        self.draw_multiplayer()

    def client(self, port, name):
        global client
        
        host = IP
        port = int(port)
        client = socket.socket()
        try:
            client.connect((host, port))
        except ConnectionRefusedError:
            self.draw_make_room()
            return
        
        print('连接成功')
    
        client.send(self.name_i.encode('utf-8'))
        self.name_u = client.recv(1024).decode('utf-8')

        self.color = client.recv(1024).decode('utf-8')

        print(self.name_u, self.color)

        receive_line = threading.Thread(target=self.receiver)
        receive_line.start()

        self.clear_multi_game()
        self.draw_multiplayer()

    def open_game(self):
        port = self.room_num.get()
        self.name_i = self.get_name.get()
        
        if len(port) == 4 and self.name_i.strip() != '':
            self.draw_wait_o()
            t = threading.Thread(target=self.server, args=(port,))
            t.start()

    def add_game(self):
        port = self.room_num.get()
        self.name_i = self.get_name.get()

        if len(port) == 4 and self.name_i.strip() != '':
            self.draw_wait_a()
            t = threading.Thread(target=self.client, args=(port,self.name_i))
            t.start()

    def multi_leave(self):
        self.draw_main()

    def send_message(self, event=None):
        message = self.input_box.get()
        if message.strip() != '':
            self.chat_box.configure(state='normal')
            self.chat_box.insert(tk.END, '<'+self.name_i+'>'+':'+message+'\n')
            self.chat_box.configure(state='disabled')
            self.chat_box.see(tk.END)
            self.input_box.delete(0, tk.END)

            client.send(('<chat_>'+message).encode('utf-8'))

    def askyesno_plus(self, title, msg, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        msg_width = 300
        msg_height = 150
        msg_x = parent_x + (parent_width - msg_width) // 2
        msg_y = parent_y + (parent_height - msg_height) // 3

        msg_box = tk.Toplevel(parent)
        msg_box.title(title)
        msg_box.geometry(f'{msg_width}x{msg_height}+{msg_x}+{msg_y}')

        msg_label = tk.Label(msg_box, text=msg, font=('', 24))
        msg_label.place(relx=0.5, rely=0.3, anchor='center')

        result = None

        def close_msg_box(choice):
            nonlocal result
            result = choice
            msg_box.destroy()

        msg_box.protocol("WM_DELETE_WINDOW", lambda: (False, close_msg_box(False)))

        yes_button = tk.Button(msg_box, text='同意', command=lambda: close_msg_box(True))
        yes_button.place(relx=1/3, rely=4/5, anchor='center', width=70, height=30)
        no_button =  tk.Button(msg_box, text='拒绝', command=lambda: close_msg_box(False))
        no_button.place(relx=2/3, rely=4/5, anchor='center', width=70, height=30)

        msg_box.wait_window(msg_box)

        return result

    def showinfo_plus(self, title, msg, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        msg_width = 300
        msg_height = 150
        msg_x = parent_x + (parent_width - msg_width) // 2
        msg_y = parent_y + (parent_height - msg_height) // 3

        msg_box = tk.Toplevel(parent)
        msg_box.title(title)
        msg_box.geometry(f'{msg_width}x{msg_height}+{msg_x}+{msg_y}')

        msg_label = tk.Label(msg_box, text=msg, font=('', 24))
        msg_label.place(relx=0.5, rely=0.3, anchor='center')

        result = None

        def close_msg_box(choice):
            nonlocal result
            result = choice
            msg_box.destroy()

        msg_box.protocol("WM_DELETE_WINDOW", lambda: close_msg_box('ok'))

        sure_button = tk.Button(msg_box, text='确认', command=lambda: close_msg_box('ok'))
        sure_button.place(relx=0.5, rely=4/5, width=70, height=30, anchor='center')

        msg_box.wait_window(msg_box)

        return result
       
game = Game()
game.draw_main()
game.board_cv.bind('<Button-1>', game.set_chess)
game.input_box.bind('<Return>', game.send_message)
game.root.mainloop()
