import tkinter

display_page_query="select * from items where QTYDesired>0;"
def send_login_page():
    top=tkinter.Tk()
    button=tkinter.Button(top,text="login",command=lambda:authenticate_user(user_box.get(),pass_box.get()))
    username_label=tkinter.Label(top,text="username")
    password_label=tkinter.Label(top,text="password")
    user_box=tkinter.Entry(top)
    pass_box=tkinter.Entry(top)
    username_label.pack()
    user_box.pack()
    password_label.pack()
    pass_box.pack()
    button.pack()
    top.mainloop()

def authenticate_user(username:str,password:str):
    raise NotImplementedError
def displayPage():

    data=[(Mike,2),(Bob,3)]
    root=tkinter.Tk()
    #for each data item insert it into the grid
    for i in range(len(data)):
            for j in range(len(data[i])):                  
                e = tkinter.Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))                 
                e.grid(row=i, column=j)
                e.insert(tkinter.END, data[i][j])
    root.mainloop()          


if __name__ == "__main__":
   displayPage()