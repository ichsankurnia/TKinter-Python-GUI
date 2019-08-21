import tkinter as tk
from tkinter import *

def createWidgets():
    font = ('Helvetica', 10)
    bg = "turquoise4"
    searchLabel = Label(root, text="Search for : ", bg=bg, font=font)
    searchLabel.grid(row=0, column=1, padx=5,
                     pady=5)  # -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky

    searchText = Entry(root, width=50, textvariable=searchnews)
    searchText.grid(row=0, column=2, padx=5, pady=5)

    searchButton = Button(root, width=20, text="Search", command=SearchNews)
    searchButton.grid(row=0, column=3, padx=5, pady=5)

    # Radio Button
    allRadioBtn = Radiobutton(text="All", variable=s, value='neutral', bg=bg, font=font)
    allRadioBtn.grid(row=1, column=1, padx=5, pady=5)

    goRadionBtn = Radiobutton(text="Good News", variable=s, value='positive', bg=bg, font=font)
    goRadionBtn.grid(row=1, column=2, padx=5, pady=5)

    baRadioBtn = Radiobutton(text="Bad News", variable=s, value='negative', bg=bg, font=font)
    baRadioBtn.grid(row=1, column=3, padx=5, pady=5)

    # Setting the default selection for the RadioButton
    s.set('neutral')

    root.newsResults = Text(root, width=70, height=30)
    root.newsResults.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

def SearchNews():
    searchFOr = searchnews.get()
    newsType = s.get()

    displayNews = ""
    root.newsResults.delete('1.0', END)

    for i in range(3):
        displayNews = "\n"+str(i)+". "+searchFOr+"\n"+newsType

        print(displayNews)
        root.newsResults.insert('1.0', displayNews)

root = tk.Tk()

root.title("Test")
root.resizable(width=False, height=False)
root.config(bg="turquoise4")
root.geometry(newGeometry="590x575")

searchnews = StringVar()
s = StringVar()

createWidgets()

root.mainloop()
