from tkinter import *
from tkinter import messagebox as msgBox

import os
import urllib.request as ulib
from bs4 import BeautifulSoup as Soup
import ast
from selenium import webdriver

# chromePath=r'C:\Windows.old\Users\Ivan\MyPythonScripts\Drivers\chromedriver.exe'
chromePath=r'C:\Users\DELL\Downloads\Programs\chromedriver.exe'

driver = webdriver.Chrome(chromePath)

def raise_frame(frame):
    frame.tkraise()


def search():
    search = searchFor.get()

    if search == "":
        msgBox.showerror(title="Empty Keywords", message="Please enter keywords to find the image")
        return FileNotFoundError

    driver.get('https://www.google.ru/search?q='+ search +'&num=1000&newwindow=1&safe=off&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiGueO-uN7eAhXCFiwKHTiYDlUQ_AUIDigB&biw=1440&bih=789')
    # a=input("Press Enter to download image")
    page = driver.page_source
    # print(page)
    # result.set(page)
    soup = Soup(page, 'lxml')
    desiredURLs = soup.findAll('div', {'class':'rg_meta notranslate'})
    ourURLs = []
    for url in desiredURLs:
        theURL = url.text
        theURL = ast.literal_eval(theURL)['ou']

        ourURLs.append(theURL)
    result.set(" ")
    return ourURLs

def download():

    num = numImages.get()
    folder = directory.get()

    if num == "":
        msgBox.showerror(title="Empty Form", message="Please enter the number of images that you want to download")
        return FileNotFoundError

    if folder == "":
        msgBox.showerror(title="Empty Form", message="Please enter the directory name to save the image first")
        return FileNotFoundError

    URLs = search()

    URLs = URLs[:int(num)]

    if not os.path.isdir(folder):
        os.mkdir(folder)

    msgBox.showinfo(title="Downloading...", message="Please wait, your image is being downloaded")

    for i, url in enumerate(URLs):
        savePath = os.path.join(folder, '{:06}.jpg'.format(i))
        # print("Downloading... {}/{} ========================== {}%".format(URLs.index(url) + 1, len(URLs), (URLs.index(url) + 1) * 100 / len(URLs)))
        result.set(" ")
        result.set("Downloading... {}/{} ========================== {}%".format(URLs.index(url) + 1, len(URLs), (URLs.index(url) + 1) * 100 / len(URLs)))
        result.set(" ")
        try:
            ulib.urlretrieve(url, savePath)
        except:
            print('I failed with', url)

    msgBox.showinfo(title="Download Complete", message="Your picture has finished downloading, Please check your "+folder+" directory now")
    result.set("Download Complete")

    searchFor.set("")
    numImages.set("")
    directory.set("")


root = Tk()

root.title("Downlaod Pictures from Google Search Images")
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
searchFor      = StringVar()
numImages        = StringVar()
directory       = StringVar()
result        = StringVar()

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
# font = ('Helvetica', 10)
# bg = "turquoise4"
Label(startPage, text="Search for : ", bg=bg, fg=fg, font=font).grid(row=0, column=1, padx=5, pady=5)  # -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky
Entry(startPage, width=50, textvariable=searchFor).grid(row=0, column=2, padx=5, pady=5)

Label(startPage, text="Number of images : ", bg=bg, fg=fg, font=font).grid(row=1, column=1, padx=5, pady=5)  # -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky
Entry(startPage, width=50, textvariable=numImages).grid(row=1, column=2, padx=5, pady=5)

Label(startPage, text="Directory name to save images : ", bg=bg, fg=fg, font=font).grid(row=2, column=1, padx=5, pady=5)  # -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky
Entry(startPage, width=50, textvariable=directory).grid(row=2, column=2, padx=5, pady=5)

Button(startPage, width=20, text="Search", command=search).grid(row=1, column=3, padx=5, pady=5)

Entry(startPage, width=70, textvariable=result).grid(row=3, column=1, columnspan=3, padx=5, pady=5)

Button(startPage, width=20, text="Download", command=download).grid(row=4, column=2, padx=5, pady=5)


""""================================================== Login Page ==================================================="""
Label(loginPage, text="Email     : ", bg=bg, fg=fg, font=font).grid(row=0, column=1, padx=5, pady=5)
Entry(loginPage, width=30, textvariable=searchFor).grid(row=0, column=2, padx=5, pady=5)

Label(loginPage, text="Password  : ", bg=bg, fg=fg, font=font).grid(row=1, column=1, padx=5, pady=5)
Entry(loginPage, width=30, textvariable=numImages).grid(row=1, column=2, padx=5, pady=5)


Button(loginPage, width=20, text="Login", command=search).grid(row=8, column=3, padx=5, pady=5)
Button(loginPage, width=20, text="Back", command=download).grid(row=8, column=2, padx=5, pady=5)
# Button(loginPage, width=20, text="Back", command=lambda:raise_frame(startPage)).grid(row=8, column=2, padx=5, pady=5)


"""================================================= Data Page ======================================================"""
Label(dataPage, text="Name  : ", bg=bg, fg=fg, font=font).grid(row=0, column=1, padx=5, pady=5)
Entry(dataPage, width=30, textvariable=dataName).grid(row=0, column=2, padx=5, pady=5)

Label(dataPage, text="N I M  : ", bg=bg, fg=fg, font=font).grid(row=1, column=1, padx=5, pady=5)
Entry(dataPage, width=30, textvariable=dataNIM).grid(row=1, column=2, padx=5, pady=5)

Label(dataPage, text="Email : ", bg=bg, fg=fg, font=font).grid(row=2, column=1, padx=5, pady=5)
Entry(dataPage, width=30, textvariable=dataEmail).grid(row=2, column=2, padx=5, pady=5)

Button(dataPage, width=20, text="Confirm", command=search).grid(row=4, column=3, padx=5, pady=5)

Button(dataPage, width=20, text="Back", command=download).grid(row=4, column=2, padx=5, pady=5)


root.mainloop()