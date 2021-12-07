import tkinter as TK

display_page_query="select * from items where QTYDesired>0;"
def send_login_page():
    top=TK.Tk()
    top.title('GiftRegistry')
    top.geometry('243x150') #Golden Ratio
    username_label=TK.Label(top,text="username")
    password_label=TK.Label(top,text="password")
    error_label=TK.Label(top,text="")
    user_box=TK.Entry(top)
    pass_box=TK.Entry(top)
    button=TK.Button(top,text="login",command=lambda:attempt_login(user_box.get(),pass_box.get(),error_label))
    username_label.pack()
    user_box.pack()
    password_label.pack()
    pass_box.pack()
    button.pack()
    error_label.pack()
    top.mainloop()

def attempt_login(username:str,password:str,errorOut:TK.Label):
    if(authenticate_user(username,password)):
        display_page()
    else:
        errorOut.config(text = "Incorrect username and/or password.", fg='#A33')

def authenticate_user(username:str,password:str):
    return False
    #raise NotImplementedError

def display_page():
    data=[("Mike",2),('Bob',3)]
    root=TK.Tk()
    #for each data item insert it into the grid
    for i in range(len(data)):
            for j in range(len(data[i])):                  
                e = TK.Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))                 
                e.grid(row=i, column=j)
                e.insert(TK.END, data[i][j])
    root.mainloop()          


if __name__ == "__main__":
   #display_page()
   send_login_page()