import tkinter as TK
import databaseInteraction
from enum import Enum


display_page_query="select * from items where QTYDesired>0;"
class Field(Enum):
    ID=1
    ITEM_DESC=2
    PRIORITY=3
    QTY_DESIRED=4
    QTY_LEFT=5
    QTY_PURCHASED=6
class Order(Enum):
    ASCENDING=1
    DESCENDING=2
def send_login_page():
    top=TK.Tk()
    top.title('GiftRegistry')
    top.geometry('243x150') #Golden Ratio
    username_label=TK.Label(top,text="username")
    password_label=TK.Label(top,text="password")
    error_label=TK.Label(top,text="")
    user_box=TK.Entry(top)
    pass_box=TK.Entry(top)
    button=TK.Button(top,text="login",command=lambda:attempt_login(user_box.get(),pass_box.get(),error_label,top))
    username_label.pack()
    user_box.pack()
    password_label.pack()
    pass_box.pack()
    button.pack()
    error_label.pack()
    top.mainloop()

def attempt_login(username:str,password:str,errorOut:TK.Label,prevWind:TK):
    if(authenticate_user(username,password)):
        prevWind.destroy()
        display_page()
    else:
        errorOut.config(text = "Incorrect username and/or password.", fg='#A33')

def authenticate_user(username:str,password:str):
    return True
    #raise NotImplementedError

def display_page(data):
    row_offset=4
    root=TK.Tk()
    name_box=TK.Entry(root)
    name_button=TK.Button(root,text="Filter by Name")

    sort_box=TK.OptionMenu(root,"id","Fields",options=Field)
    order_box=TK.OptionMenu(root,"id","Order",options=Order)
    sort_button=TK.Button(root,text="Sort By Field")
    low_price_box=TK.Entry(root,text="Min price")
    low_price_box.insert(0,"Min price")
    upper_price_box=TK.Entry(root,text="Max price")
    upper_price_box.insert(0,"Max price")
    filter_price_button=TK.Button(root,text="Filter by Price")
    priority_box=TK.Entry(root)
    priority_button=TK.Button(root,text="Filter by Minimum priority")
    name_box.grid(row=0,column=0)
    name_button.grid(row=0,column=1)
    sort_box.grid(row=1,column=0)
    sort_button.grid(row=1,column=1)
    low_price_box.grid(row=2,column=0)
    upper_price_box.grid(row=2,column=1)
    filter_price_button.grid(row=2,column=2)
    priority_box.grid(row=3,column=0)
    priority_button.grid(row=3,column=1)
    #for each data item insert it into the grid
    for i in range(len(data)):
            for j in range(len(data[i])):                  
                e = TK.Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))                 
                e.grid(row=i+row_offset, column=j)
                e.insert(TK.END, data[i][j])
    root.mainloop()    
    display=root


if __name__ == "__main__":
   display_page([["bob",3,"t",2,5],["mike",2,"B",5,6]])
   send_login_page()
