import signal
import sys,time,os
import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from setting import Setting
from multiprocessing import Process
from threading import Thread
from run_game import run_game
import easygui

signal.signal(signal.SIGCHLD,signal.SIG_IGN)

st = Setting()

class Client():
    def __init__(self,table):
        self.client = socket.socket()
        self.client.connect((st.server_ip,st.server_port))
        self.username = easygui.enterbox('Your username')
        self.p_ls = []
        self.best_score = 0
        self.table = table
        self.id_identify = []
        self.is_in_online = False

    def run(self):
        pass

    def login_verify(self):
        while True:
            if self.is_in_online:
                easygui.msgbox("username already online")
                self.username = easygui.enterbox('Your username')
                self.client.send(('home ' + self.username).encode())
                while True:
                    data = self.client.recv(st.recv_max_bytes).decode()
                    if data != 'U online':
                        self.is_in_online = False
                        return data
                    easygui.msgbox("username already online")
                    self.username = easygui.enterbox('Your username')
                    self.client.send(('home ' + self.username).encode())

            if not self.username:
                easygui.msgbox("username can't be null")
                self.username = easygui.enterbox('Your username')
            elif len(self.username) < 3 or len(self.username) > 15:
                easygui.msgbox('username must be greater than 3 or 15 characters.')
                self.username = easygui.enterbox('Your username')
            elif self.username == ' ' * len(self.username) or self.username == '.' * len(self.username):
                easygui.msgbox('Invalid character')
                self.username = easygui.enterbox('Your username')
            else:
                break

    def show_main_data(self):
        val = None
        self.login_verify()
        self.client.send(('home ' + self.username).encode())
        data = self.client.recv(st.recv_max_bytes).decode()
        print(data)
        if data == 'U online':
            self.is_in_online = True
            val = self.login_verify()
        if data == 'No data!' or val == 'No data!':
            self.table.insert('',tk.END,values=['No data','NULL','NULL','NULL'])
        elif val != 'No data!' and val:
            data_ls = eval(val)
            print(data_ls)
            data_ls.sort(key=lambda x:x[2], reverse=True)
            for d in data_ls:
                if d[1] == self.username:
                    self.best_score = d[2]
                item_id = self.table.insert('', tk.END, values=d)
                temp = [item_id] + list(d)
                self.id_identify.append(temp)
        else:
            data_ls = eval(data)
            print(data_ls)
            data_ls.sort(key=lambda x: x[2], reverse=True)
            for d in data_ls:
                if d[1] == self.username:
                    self.best_score = d[2]
                item_id = self.table.insert('', tk.END, values=d)
                temp = [item_id] + list(d)
                self.id_identify.append(temp)

    def change_data(self):
        while True:
            data = self.client.recv(st.recv_max_bytes).decode()
            if data.startswith('change ok'):
                b_s = data.split('change ok',1)[1]
                for val in self.id_identify:
                    if val[2] == self.username:
                        val[3] = int(b_s)
                        val[4] = int(b_s) // 10
                        self.table.set(val[0],column='Best score',value=val[3])
                        self.table.set(val[0],column='Count',value=val[4])
                        break
                for child in self.table.get_children():
                    self.table.delete(child)
                self.id_identify.sort(key=lambda x:x[3],reverse=True)
                for val in self.id_identify:
                    val[0] = self.table.insert('',tk.END,value=val[1:])
                self.best_score = int(b_s)


    def on_quit_main_window(self,window):
        self.client.send(str(['q',self.username]).encode())
        self.client.close()
        window.destroy()


    def run_game(self,window):
        p = Process(target=run_game,args=(self.client,window,self.best_score,self.username))
        self.p_ls.append(p)
        p.start()



def login_window(client):
    l_window = tk.Tk()
    l_window.title('Login')
    l_window.geometry('400x300+{}+{}'.format(l_window.winfo_screenwidth() // 3,l_window.winfo_screenheight() // 4))
    l_window.resizable(0,0)
    l_window.protocol("WM_DELETE_WINDOW",lambda :client.on_quit_login_window(l_window))
    user_label = tk.Label(l_window,text='Username',font=(None,15,'bold'))
    user_label.place(x=30,y=30)
    user_enter = tk.Entry(l_window,width=20,font=(None,15))
    user_enter.place(x=30,y=60)

    pwd_label = tk.Label(l_window, text='Password', font=(None, 15, 'bold'))
    pwd_label.place(x=30, y=100)
    pwd_enter = tk.Entry(l_window, width=20, font=(None, 15))
    pwd_enter.place(x=30, y=130)

    login_button = tk.Button(l_window,text='Login',font=(None,15),width=18)
    login_button.place(x=30,y=190)

    l_window.mainloop()


def main_window():
    window = tk.Tk()
    window.title("Snake user info")
    window.resizable(0,0)
    window.geometry('500x600+{}+{}'.format(window.winfo_screenwidth() // 3,window.winfo_screenheight() // 4))
    window.columnconfigure(0,weight=1)
    window.protocol("WM_DELETE_WINDOW",lambda :client.on_quit_main_window(window))

    user_label = tk.Label(window,text='User Content',font=(None,20,'bold'))
    user_label.place(x=160,y=20)

    columns = ['User_id', 'Username', 'Best score', 'Count']
    table = ttk.Treeview(
            master=window,
            height=20,
            columns=columns,
            show='headings',
    )

    table.heading(column='User_id', text='User_id')
    table.heading('Username', text='Username')
    table.heading('Best score', text='Best score')
    table.heading('Count', text='Count')

    table.column('User_id', width=120, minwidth=120,anchor=tk.CENTER)
    table.column('Username', width=120, minwidth=120,anchor=tk.CENTER)
    table.column('Best score', width=120, minwidth=120,anchor=tk.CENTER)
    table.column('Count', width=120, minwidth=120,anchor=tk.CENTER)

    yscroll = tk.Scrollbar(window, orient=tk.VERTICAL,command=table.yview)
    table.configure(yscrollcommand=yscroll.set)
    yscroll.pack(side=tk.RIGHT, fill=tk.Y)

    table.place(x=10,y=80)


    client = Client(table)

    button = tk.Button(window,text='Start Game',font=(None,20),bg='#0e88c4',fg='white',
                       command=lambda :client.run_game(window))
    button.place(x=170,y=530)

    client.show_main_data()

    t3 = Thread(target=client.change_data)
    t3.daemon = True
    t3.start()

    window.mainloop()


main_window()

