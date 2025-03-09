from tkinter import *
from icecream import ic
def pass_func(*args):
    ic()
def male_button_handler():
    ic('male_button_handler')
def female_button_handler():
    ic('female_button_handler')
    
if __name__ == "__main__": 
    master = Tk()
    username_Label = Label(master, text='Username')
    password_Label = Label(master, text='Password')
    username_Label.place(x=1,y=1)
    password_Label.place(x=100,y=15)
    username_Entry = Entry(master)
    password_Entry = Entry(master)
    password_Entry.bind('<Return>', pass_func)
    username_Entry.place(x=50, y=30)
    password_Entry.place(x=70, y=45)
    print("Hello!")
    var1 = IntVar()
    male_button = Checkbutton(master, text='male', variable=var1, command = male_button_handler)
    male_button.place(x=0, y=0)
    var2 = IntVar()
    female_button = Checkbutton(master, text='female', variable=var2, command = female_button_handler)
    female_button.place(x=50, y=0)
    mainloop()