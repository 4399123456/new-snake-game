import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

window = tk.Tk()
window.title("Snake user info")
window.resizable(0,0)
window.geometry('500x600+{}+{}'.format(window.winfo_screenwidth() // 3,window.winfo_screenheight() // 4))
window.columnconfigure(0,weight=1)

user_label = tk.Label(window,text='User Content',font=(None,20,'bold'))
user_label.place(x=160,y=20)

data = [
    [1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alicefsasdfasdfasdf',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8],
    [1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alicefsasdfasdfasdf',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8],
    [1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alicefsasdfasdf',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8],[1,'ken',50,5],
    [2,'steve',40,4],
    [3,'Alice',80,8]
]
data.sort(key=lambda x:x[2],reverse=True)



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


for d in data:
    table.insert('',tk.END,values=d)

button = tk.Button(window,text='Start Game',font=(None,20),bg='#0e88c4',fg='white')
button.place(x=170,y=530)

window.mainloop()



