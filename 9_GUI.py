from tkinter import *
from tkinter import messagebox as msgBox
import ttkcalendar
import tkSimpleDialog


def raise_frame(frame):
    frame.tkraise()


"""======================= Class Calendar ======================="""
class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection


"""================================================== Create Data ==================================================="""
def saveData():

    msgBox.showinfo(title="Success", message="Save data successfully")
    msgBox.showwarning(title="Attention", message="Take Your Photo!!!")

    msgBox.showinfo(title="Success", message="All your data has been saved")
    msgBox.showwarning(title="Attention", message="Please wait a moment")

    print('Trainning Success')
    msgBox.showinfo(title="Success", message="All your data has been trained")

    raise_frame(startPage)

def calendar():
    cd = CalendarDialog(signPage)
    a = str(cd.result)
    date = a[:10]
    birthE.set(date)


"""=========================================== Face Recognition ====================================================="""
def absents():
    msgBox.showinfo(title="Success", message="Get data Successfully\nCheck your data correctly and make sure is that you!!")

    raise_frame(absentsPage)


"""=========================================== Confirm Absents Page ================================================="""
def sendData():
    msgBox.showinfo(title="Success", message="Absent Success!!")

    raise_frame(startPage)


root = Tk()

root.title("Test")
# root.resizable(width=False, height=False)
root.config(bg="black")
# root.geometry(newGeometry="590x575")

font = ('Helvetica', 10)
bg = "black"
fg = "white"

startPage = Frame(root, bg="black") # , width=100, height=100
signPage = Frame(root, bg="black")
absentsPage = Frame(root, bg="black")
f4 = Frame(root, bg="black")

"""Buat Data"""
nameE       = StringVar()
nimE        = StringVar()
classE      = StringVar()
birthE      = StringVar()
genderE     = StringVar()
addressE    = StringVar()
telpE       = StringVar()
emailE      = StringVar()

dropdown    = StringVar()


"""Tampillin di absen page"""
absName     = StringVar()
absNIM      = StringVar()
absClass    = StringVar()



"""=================================================================================================================="""
for frame in (startPage, signPage, absentsPage, f4):
    frame.grid(row=0, column=0,sticky='news')

Label(f4, text='FRAME 4').pack(side='right')
Button(f4, text='Back to frame 1', command=lambda:raise_frame(startPage)).pack(side='right')

raise_frame(startPage)



"""" ============================================= Start Page GUI ==================================================="""
Button(startPage, width=20, text="Sign Up", command=lambda:raise_frame(signPage)).grid(row=3, column=3, padx=5, pady=5)

Button(startPage, width=20, text="Do Absent", command=absents).grid(row=5, column=0, padx=5, pady=5)



""""================================================ Sign Up Page ==================================================="""
Label(signPage, text="Name  : ", bg=bg, fg=fg, font=font).grid(row=0, column=1, padx=5, pady=5)
Entry(signPage, width=30, textvariable=nameE).grid(row=0, column=2, padx=5, pady=5)

Label(signPage, text="N I M  : ", bg=bg, fg=fg, font=font).grid(row=1, column=1, padx=5, pady=5)
Entry(signPage, width=30, textvariable=nimE).grid(row=1, column=2, padx=5, pady=5)

Label(signPage, text="Class : ", bg=bg, fg=fg, font=font).grid(row=2, column=1, padx=5, pady=5)
choices = { 'EC2A','EC2B','EC2C','EC2D','IKI2', 'EC4A', 'EC4B', 'EC4C', 'EC4D', 'IKI4', 'EC6A', 'EC6B', 'EC6C', 'EC6D', 'IKI6', 'IKI8'}
dropdown.set('Tap Here') # set the default option

popupMenu = OptionMenu(signPage, dropdown, *choices).grid(row = 2, column =2, padx=5, pady=5)

def change_dropdown(*args):
    kelas = dropdown.get()
    classE.set(kelas)
    # print(kelas)

dropdown.trace('w', change_dropdown)

Label(signPage, text="Date of Birth : ", bg=bg, fg=fg, font=font).grid(row=3, column=1, padx=5, pady=5)
Button(signPage, width=25, text="Click Here", command=calendar, textvariable=birthE).grid(row=3, column=2, padx=5, pady=5)

Label(signPage, text="Gender : ", bg=bg, fg=fg, font=font).grid(row=4, column=1, padx=5, pady=5)
Radiobutton(signPage,text="Man", variable=genderE, value='L', bg="white", font=font).grid(row=4, column=2, padx=5, pady=5)
Radiobutton(signPage, text="Woman", variable=genderE, value='P', bg="white", font=font).grid(row=4, column=3, padx=5, pady=5)
genderE.set('L')

Label(signPage, text="Address : ", bg=bg, fg=fg, font=font).grid(row=5, column=1, padx=5, pady=5)
Entry(signPage, width=30, textvariable=addressE).grid(row=5, column=2, padx=5, pady=5)

Label(signPage, text="Telp : ", bg=bg, fg=fg, font=font).grid(row=6, column=1, padx=5, pady=5)
Entry(signPage, width=30, textvariable=telpE).grid(row=6, column=2, padx=5, pady=5)

Label(signPage, text="E-mail : ", bg=bg, fg=fg, font=font).grid(row=7, column=1, padx=5, pady=5)
Entry(signPage, width=30, textvariable=emailE).grid(row=7, column=2, padx=5, pady=5)

Button(signPage, width=20, text="Save", command=saveData).grid(row=8, column=3, padx=5, pady=5)

Button(signPage, width=20, text="Back", command=lambda:raise_frame(startPage)).grid(row=8, column=2, padx=5, pady=5)



"""============================================== Absents Page ======================================================"""
Label(absentsPage, text="Name  : ", bg=bg, fg=fg, font=font).grid(row=0, column=1, padx=5, pady=5)
Entry(absentsPage, width=30, textvariable=absName).grid(row=0, column=2, padx=5, pady=5)

Label(absentsPage, text="N I M  : ", bg=bg, fg=fg, font=font).grid(row=1, column=1, padx=5, pady=5)
Entry(absentsPage, width=30, textvariable=absNIM).grid(row=1, column=2, padx=5, pady=5)

Label(absentsPage, text="Class : ", bg=bg, fg=fg, font=font).grid(row=2, column=1, padx=5, pady=5)
Entry(absentsPage, width=30, textvariable=absClass).grid(row=2, column=2, padx=5, pady=5)

Button(absentsPage, width=20, text="Confirm", command=sendData).grid(row=4, column=3, padx=5, pady=5)

Button(absentsPage, width=20, text="Try Again", command=absents).grid(row=4, column=2, padx=5, pady=5)



root.mainloop()