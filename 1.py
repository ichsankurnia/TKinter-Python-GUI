import tkinter as tk
import tkinter.messagebox as msgBox
# from tkinter import messagebox
import tkinter.font as tkfont

main_windows = tk.Tk()
# frame_button = tk.Frame(main_windows)
# frame_button.pack(side=tk.BOTTOM)

font = tkfont.Font(family="Helvetica",size=36,weight="bold",underline=1,slant="italic",overstrike=1)

textLabel = 'Hello World'
label = tk.Label(text=textLabel, font=font, relief=tk.RIDGE, bg="black", fg="green")
label.pack(side=tk.TOP)

text = tk.StringVar()
label1 = tk.Label(textvariable=text, relief=tk.RAISED ) #relief itu ngasih gaya2, kaya buttin

text.set("Hey!? How are you today?")
label1.pack(anchor=tk.N)    # anchor itu posisi N = North

L1 = tk.Label(text="User Name")
L1.pack(side=tk.LEFT)
E1 = tk.Entry(bd =5)
E1.pack(side = tk.LEFT)

def CallBack():
    msgBox.showinfo(title="Hello Python", message="Hello World")
    msgBox.showwarning(title='Warning!!!', message='Something Occured on your program')
    msgBox.showerror(title='Error', message='i dont know what i want to do')

buton = tk.Button(text ="Hello", command = CallBack, fg='blue')
buton.pack(side=tk.TOP)

B1 = tk.Button(text ="FLAT", highlightcolor="black", relief=tk.FLAT )
B2 = tk.Button(text ="RAISED", relief=tk.RAISED, cursor='heart' )
B3 = tk.Button(text ="SUNKEN", relief=tk.SUNKEN )
B4 = tk.Button(text ="GROOVE", relief=tk.GROOVE )
B5 = tk.Button(text ="RIDGE", relief=tk.RIDGE )

B1.pack(side=tk.TOP)
B2.pack(side=tk.TOP)
B3.pack(side=tk.TOP)
B4.pack(side=tk.TOP)
B5.pack(side=tk.TOP)

list=[1,3,5,7]
w = tk.Spinbox(from_=list[0], to=list[3])
w.pack()

main_windows.mainloop()