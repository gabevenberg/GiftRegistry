import tkinter as TK
import databaseInteraction
import logging
from enum import Enum

logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)

display_page_query="select * from items where QTYDesired>0;"
class Field(Enum):
    ID=1
    ITEM_DESC=2
    PRIORITY=3      
    QTY_LEFT=4
   
class Order(Enum):
    ASCENDING=1
    DESCENDING=2
def send_login_page(inDB, inconfig):
    logging.debug('login page called')
    global DB
    global config
    DB=inDB
    config=inconfig
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

def filter_by_name(name:str):
    data=DB.fitlerByName(name)
    display(data)
def filter_by_priority(priority:int):
    data=DB.filterByPriority(priority)
    display(data)
def filter_by_price(upper:int,lower:int):
    data=DB.filterByPrice(upper,lower)
    display(data)
def sort_entries(field:Field,order:Order):
    data=DB.sortEntries(field,order)
    display(data)
def attempt_login(username:str,password:str,errorOut:TK.Label,prevWind:TK):
    logging.debug('attempting login')
    if(authenticate_user(username,password)):
        logging.debug('login sucsessfull, destroying window')
        prevWind.destroy()
        logging.debug('calling displayPage')
        display_page(DB.getUnpurchasedGifts)
    else:
        logging.debug('login failed')
        errorOut.config(text = "Incorrect username and/or password.", fg='#A33')

def authenticate_user(username:str,password:str):
    return True
    #raise NotImplementedError

def display_purchase_page(items_purchased:list):
    page=TK.Tk()
    
    purchase_display=TK.Label(page,"You purchased: ")
    purchase_display.grid(row=0,column=0)
    for i in len(items_purchased):
        d=TK.Label(page,items_purchased[i])
        d.grid(row=i+1,column=0)
    return_page=TK.Button(page,"Return to Table")
    return_page.grid(row=len(items_purchased+1),column=0)
def display_page(data):
    row_offset=5
    root=TK.Tk()
    default_button=TK.Button(root,"Return to default filters",command=display_page(DB.getUnpurchasedGifts()))
    checks=len(data)*[None]
    name_box=TK.Entry(root)
    breakpoint()
    name_button=TK.Button(root,text="Filter by Name",command=lambda:filter_by_name(name_box.get()))

    sort_box=TK.OptionMenu(root,"id","Fields",options=Field)
    order_box=TK.OptionMenu(root,"id","Order",options=Order)
    breakpoint()
    sort_button=TK.Button(root,text="Sort By Field",command=lambda:sort_entries(sort_box.get()))
    low_price_box=TK.Entry(root,text="Min price")
    low_price_box.insert(0,"Min price")
    upper_price_box=TK.Entry(root,text="Max price")
    upper_price_box.insert(0,"Max price")
    breakpoint()
    filter_price_button=TK.Button(root,text="Filter by Price",command=lambda:filter_by_price(upper_price_box.get(),low_price_box.get()))
    priority_box=TK.Entry(root)
    breakpoint()
    priority_button=TK.Button(root,text="Filter by Minimum priority",command=lambda:filter_by_priority(priority_box.get()))
    breakpoint()
    purchase_button=TK.Button(root,text="Purchase Selected Item",command=lambda:display_purchase_page(filter(lambda x:x.value(),checks)))
    name_box.grid(row=0,column=0)
    name_button.grid(row=0,column=1)
    sort_box.grid(row=1,column=0)
    sort_button.grid(row=1,column=1)
    low_price_box.grid(row=2,column=0)
    upper_price_box.grid(row=2,column=1)
    filter_price_button.grid(row=2,column=2)
    priority_box.grid(row=3,column=0)
    priority_button.grid(row=3,column=1)
    purchase_button.grid(row=4,column=0)
    breakpoint()
    #for each data item insert it into the grid
    for i in range(len(data)):      
            check=TK.Checkbutton(var=checks[i])
            check.grid(row=i+row_offset,column=0)
            for j in range(len(data[i])):  
                e = TK.Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))                
                e.grid(row=i+row_offset, column=j+1)
                e.insert(TK.END, data[i][j])
    breakpoint()
    root.mainloop()    
    display=root


if __name__ == "__main__":
   display_page([["bob",3,"t",2,5],["mike",2,"B",5,6]])
   send_login_page()
