from tkinter import *
import tkinter as tk
from tkinter.ttk import *

root = Tk()
root.title("Tk dropdown example")

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

# Create a Tkinter variable
tkvar = StringVar(root)
var = StringVar(root)

# Dictionary with options
choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
tkvar.set('Pizza') # set the default option

Label(mainframe, text="Choose a dish").grid(row = 1, column = 1)
popupMenu = OptionMenu(mainframe, tkvar, *choices)
popupMenu.grid(row = 2, column =1)

Entry(mainframe, textvariable=var).grid(row=1, column=2)

# on change dropdown value
def change_dropdown(*args):
    food = tkvar.get()
    var.set(food)
    print(food)

# link function to change dropdown
tkvar.trace('w', change_dropdown)

root.mainloop()