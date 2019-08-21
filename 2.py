from tkinter import *

root = Tk()

header = Frame(root)
header.pack()

footer = Frame(root)
footer.pack(side=BOTTOM)

button1 = Button(header, text="Button1", fg="blue")
button2 = Button(header, text="Button2", fg="green")
button3 = Button(footer, text="Button3", fg="red")
button4 = Button(footer, text="Button4", fg="yellow")

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=RIGHT)

text1 = Label(root, bg='red', fg='white', text="TEst")
text1.pack(fill=X)
text1 = Label(root, bg='red', fg='white', text="TEst")
text1.pack(side=LEFT,fill=Y)

root.mainloop()