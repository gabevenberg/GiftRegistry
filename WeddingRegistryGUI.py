import tkinter as TK
from tkinter import messagebox
import logging
import webbrowser
from functools import partial
from enum import Enum
from tkinter.constants import DISABLED

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
    pass_box=TK.Entry(top,show='*')
    button=TK.Button(top,text="login",command=lambda:attempt_login(user_box.get(),pass_box.get(),error_label,top))
    username_label.pack()
    user_box.pack()
    password_label.pack()
    pass_box.pack()
    button.pack()
    error_label.pack()
    top.mainloop()

def filter_by_name(name,root:TK.Tk):
    data=DB.fitlerByName(name())
    root.destroy()
    display_page(data)
def filter_by_priority(priority,root:TK.Tk):
    logging.debug('prioFilter '+priority())
    data=DB.filterByPriority(priority())
    root.destroy()
    display_page(data)
def filter_by_price(upper,lower,root:TK.Tk):
    data=DB.filterByPrice(upper(),lower())
    root.destroy()
    display_page(data)
def sort_entries(field:Field,order:Order,root:TK.Tk):
    data=DB.sortEntries(field,order)
    root.destroy()
    display_page(data)
def attempt_login(username:str,password:str,errorOut:TK.Label,prevWind:TK):
    logging.debug('attempting login')
    if(authenticate_user(username,password)):
        logging.debug('login sucsessfull, destroying window')
        prevWind.destroy()
        logging.debug('calling displayPage')
        display_page(DB.getUnpurchasedGifts())
    else:
        logging.debug('login failed')
        errorOut.config(text = "Incorrect username and/or password.", fg='#A33')

def authenticate_user(username:str,password:str):
    return DB.validateUser(username, password)[0]
    #raise NotImplementedError

def display_purchase_page(items_purchased:list):
    page=TK.Tk()
    
    purchase_display=TK.Label(page,text="You purchased: ")
    purchase_display.grid(row=0,column=0)
    for i in range(len(items_purchased)):
        d=TK.Label(page,items_purchased[i])
        d.grid(row=i+1,column=0)
    return_page=TK.Button(page,text="Return to Table")
    return_page.grid(row=len(items_purchased+1),column=0)
def display_page(data):
    row_offset=6
    root=TK.Tk()
    # logging.debug('making default_button')
    # default_button=TK.Button(root,"Return to default filters",command=display_page(DB.getUnpurchasedGifts()))
    name_box=TK.Entry(root)
    logging.debug('calling filter_by_name')
    name_button=TK.Button(root,text="Filter by Name",command=partial(filter_by_name, name_box.get, root))
    sort_box=TK.OptionMenu(root,"id","Fields",*[x.name for x in Field])
    order_box=TK.OptionMenu(root,"id","Order",*[x.name for x in Order])
    logging.debug('calling sort_entries')
    # sort_button=TK.Button(root,text="Sort By Field",command=partial(sort_entries, sort_box.get()))
    low_price_box=TK.Entry(root,text="Min price")
    low_price_box.insert(0,"Min price")
    upper_price_box=TK.Entry(root,text="Max price")
    upper_price_box.insert(0,"Max price")
    logging.debug('calling filter_by_price')
    filter_price_button=TK.Button(root,text="Filter by Price",command=partial(filter_by_price,upper_price_box.get,low_price_box.get, root))
    priority_box=TK.Entry(root)
    logging.debug('calling filter_by_priority')
    priority_button=TK.Button(root,text="Filter by Priority",command=partial(filter_by_priority,priority_box.get, root)) #TODO clearer button text for filtering to lower numbers which indicate higher priority
    logging.debug('calling display_purchase_page')
    # purchase_button=TK.Button(root,text="Purchase Selected Item",command=display_purchase_page((lambda x:x.value(),checks)))
    
    name_box.grid(row=1,column=0)
    name_button.grid(row=2,column=0)

    priority_box.grid(row=1,column=1)
    priority_button.grid(row=2,column=1)
    
    # low_price_box.grid(row=1,column=2)
    # upper_price_box.grid(row=0,column=2)
    # filter_price_button.grid(row=2,column=2)

    # sort_box.grid(row=1,column=3)
    # sort_button.grid(row=2,column=3)
    
    # purchase_button.grid(row=4,column=0)
    logging.debug('calling filter_by_name')
    #for each data item insert it into the grid
    logging.debug(f'data is {len(data)} long')
    descHeader=TK.Label(root, width=20, fg='black', font=('Arial',16,), text='Item')
    descHeader.grid(row=row_offset-1, column=0)
    priorityHeader=TK.Label(root, width=20, fg='black', font=('Arial',16,), text='Preference')
    priorityHeader.grid(row=row_offset-1, column=1)
    qtyHeader=TK.Label(root, width=20, fg='black', font=('Arial',16,), text='Quantity desired')
    qtyHeader.grid(row=row_offset-1, column=2)
    for i in range(len(data)):      
        logging.debug(f'printing {data[i]}')
        desc = TK.Label(root, width=20, fg='black', font=('Arial',16,), text=data[i][1])
        priority = TK.Label(root, width=20, fg='black', font=('Arial',16,), text=data[i][2])
        qtyLeft = TK.Label(root, width=20, fg='black', font=('Arial',16,), text=data[i][3])
        purchaseLink = TK.Label(root, width=20, fg='blue', font=('Arial',16, 'underline'), text='View Item')
        logging.debug(f'putting in grid')
        desc.grid(row=i+row_offset, column=0)
        priority.grid(row=i+row_offset, column=1)
        qtyLeft.grid(row=i+row_offset, column=2)
        purchaseLink.grid(row=i+row_offset, column=3)
        purchaseLink.bind(f'<Button-{i+1}>', lambda e: webbrowser.open_new_tab(data[i][5]))
        purchaseButton=TK.Button(root, text='purchase this item', command=partial(purchasePopup,data[i], root))
        purchaseButton.grid(row=i+row_offset, column=4)
    root.mainloop()    
    display=root

def purchasePopup(item, root):
    if messagebox.askyesno(title='purchase', message=f'Did you purchase {item[1]}?'):
        popup=TK.Toplevel(root)
        popup.geometry=('200x100')
        popup.title('Amount purchased')
        amountBox=TK.Entry(popup, width=25)
        submitLabel=TK.Button(popup, text='submit my purchase', command=lambda:[DB.purchaseItem(item[0], 2, int(amountBox.get())), popup.destroy(), redraw_display_page(root)])
        amountBox.pack()
        submitLabel.pack()
    else:
        return

def redraw_display_page(window):
    window.destroy()
    display_page(DB.getUnpurchasedGifts())


if __name__ == "__main__":
   display_page([["bob",3,"t",2,5],["mike",2,"B",5,6]])
   send_login_page()
