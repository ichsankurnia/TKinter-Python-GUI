from tkinter import *
from UI_Login_from_DBServer.database import DataBase
from UI_Login_from_DBServer.jcon import updateJson
# import urllib.request, json
from tkinter import messagebox as msgBox


def raise_frame(frame):
    frame.tkraise()

def goToLoginPage():
    updateJson()
    raise_frame(loginPage)


def back():
    pwdE.set("")
    emailE.set("")
    dataEmail.set("")
    dataNIM.set("")
    dataEmail.set("")

    raise_frame(startPage)


"""====================================================== Login ====================================================="""
def loginData():
    db = DataBase("login.txt")

    email = emailE.get()
    pwd = pwdE.get()

    if db.validate(email, pwd):
        msgBox.showinfo(title="Success", message="Login Success")

        # db = DataBase("login.txt")
        email = emailE.get()
        password, name, created = db.get_user(email)

        dataName.set(name)
        dataNIM.set(created)
        dataEmail.set(email)

        pwdE.set("")
        emailE.set("")

        raise_frame(dataPage)

    else:
        msgBox.showerror(title="Failed", message="Invalid username or password")

"""=========================================== Confirm Send Page ================================================="""
def sendData():
    msgBox.showinfo(title="Success", message="Send data Success")

    raise_frame(startPage)


root = Tk()

root.title("Security Camera")
# root.resizable(width=False, height=False)
root.config(bg="black")
# root.geometry(newGeometry="590x575")

font = ('Helvetica', 10)
bg = "black"
fg = "white"

startPage = Frame(root, bg="black") # , width=100, height=100
loginPage = Frame(root, bg="black")
dataPage = Frame(root, bg="black")
f4 = Frame(root, bg="black")

"""var login"""
emailE      = StringVar()
pwdE        = StringVar()

"""var data"""
dataName     = StringVar()
dataNIM      = StringVar()
dataEmail    = StringVar()



"""=================================================================================================================="""
for frame in (startPage, loginPage, dataPage, f4):
    frame.grid(row=0, column=0,sticky='news')

Label(f4, text='FRAME 4').pack(side='right')
Button(f4, text='Back to frame 1', command=lambda:raise_frame(startPage)).pack(side='right')

raise_frame(startPage)



"""" ============================================= Start Page GUI ==================================================="""
Button(startPage, width=20, text="Login Page", command=goToLoginPage).grid(row=3, column=3, padx=5, pady=5)

Button(startPage, width=20, text="None", command=lambda:raise_frame(startPage)).grid(row=5, column=0, padx=5, pady=5)


""""================================================== Login Page ==================================================="""
Label(loginPage, text="Email     : ", bg=bg, fg=fg, font=font).grid(row=0, column=1, padx=5, pady=5)
Entry(loginPage, width=30, textvariable=emailE).grid(row=0, column=2, padx=5, pady=5)

Label(loginPage, text="Password  : ", bg=bg, fg=fg, font=font).grid(row=1, column=1, padx=5, pady=5)
Entry(loginPage, width=30, textvariable=pwdE).grid(row=1, column=2, padx=5, pady=5)


Button(loginPage, width=20, text="Login", command=loginData).grid(row=8, column=3, padx=5, pady=5)
Button(loginPage, width=20, text="Back", command=back).grid(row=8, column=2, padx=5, pady=5)
# Button(loginPage, width=20, text="Back", command=lambda:raise_frame(startPage)).grid(row=8, column=2, padx=5, pady=5)


"""================================================= Data Page ======================================================"""
Label(dataPage, text="Name  : ", bg=bg, fg=fg, font=font).grid(row=0, column=1, padx=5, pady=5)
Entry(dataPage, width=30, textvariable=dataName).grid(row=0, column=2, padx=5, pady=5)

Label(dataPage, text="N I M  : ", bg=bg, fg=fg, font=font).grid(row=1, column=1, padx=5, pady=5)
Entry(dataPage, width=30, textvariable=dataNIM).grid(row=1, column=2, padx=5, pady=5)

Label(dataPage, text="Email : ", bg=bg, fg=fg, font=font).grid(row=2, column=1, padx=5, pady=5)
Entry(dataPage, width=30, textvariable=dataEmail).grid(row=2, column=2, padx=5, pady=5)

Button(dataPage, width=20, text="Confirm", command=sendData).grid(row=4, column=3, padx=5, pady=5)

Button(dataPage, width=20, text="Back", command=back).grid(row=4, column=2, padx=5, pady=5)


root.mainloop()