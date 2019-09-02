import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox as msgBox
import ttkcalendar
import tkSimpleDialog
import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageTk
import imutils
import imutils.paths as paths
import pickle
import requests
import json
import time
import datetime


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
    path ="images\\"

    name        = nameE.get()
    nim         = nimE.get()
    kelas       = classE.get()
    tgl_lahir   = birthE.get()
    gender      = genderE.get()
    alamat      = addressE.get()
    telp        = telpE.get()
    email       = emailE.get()
    # print(name + "\n" + nim + "\n" + kelas)

    """Create target Directory"""
    try:
        os.mkdir(path + str(name))
        print("Directory ", path + str(name), " Created ")

    except FileExistsError:
        print("Directory ", path + str(name), " already exists")

    """Write Data JSON"""
    data = {}
    data['bio'] = [
        {"Name": name, "N I M": nim, "Class": kelas, "Date of Birth": tgl_lahir, "Gender":gender, "Address":alamat, "Telp": telp, "E-Mail":email},
    ]

    with open('images/' + name + '/data.txt', 'w') as file:
        json.dump(data, file)


    """============================ Send Data into Server ==========================="""
    # url = "http://localhost/presensi/input_data.php"
    # payload  = {'name': name, 'nim': nim, 'class': kelas, 'birth':tgl_lahir, 'gender':gender, 'address':alamat, 'telp':telp, 'email':email}
    # r = requests.post(url, data = payload)
    # print(r.text)

    msgBox.showinfo(title="Success", message="Save data successfully")
    msgBox.showwarning(title="Attention", message="Take Your Photo!!!")


    """======================================== Take photos ================================================"""
    face_cascade = cv2.CascadeClassifier('face-detect.xml')
    cam = cv2.VideoCapture(1)

    sampleN = 0
    while True:
        ret, frame = cam.read()
        # frame = img.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        for x, y, w, h in faces:
            cv2.imwrite(path + str(name) + "/" + str(sampleN) + ".jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            sampleN = sampleN + 1
            cv2.waitKey(200)

        cv2.imshow('img', frame)

        cv2.waitKey(1)
        if sampleN > 29:
            break

    cam.release()
    cv2.destroyAllWindows()

    msgBox.showinfo(title="Success", message="All your data has been saved")
    msgBox.showwarning(title="Attention", message="Please wait a moment")

    """====================================== Train Image ========================================="""
    dataset = "images\\"
    module = "pickle\\encoding1.pickle"
    imagepaths = list(paths.list_images(dataset))
    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagepaths):
        # print("[INFO] processing image {}/{}".format(i + 1, len(imagepaths)))
        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
            # print("[INFO] serializing encodings...")
            data = {"encodings": knownEncodings, "names": knownNames}
            output = open(module, "wb")
            pickle.dump(data, output)
            output.close()

    print('Trainning Success')
    msgBox.showinfo(title="Success", message="All your data has been trained")

    nimE.set("")
    classE.set("")
    birthE.set("")
    telpE.set("")
    addressE.set("")
    emailE.set("")
    nameE.set("")

    raise_frame(startPage)

def calendar():
    cd = CalendarDialog(signPage)
    a = str(cd.result)
    date = a[:10]
    birthE.set(date)


"""=========================================== Face Recognition ====================================================="""
def absents():
    encoding = "pickle\\encoding1.pickle"
    data = pickle.loads(open(encoding, "rb").read())
    # print(data)
    # {'encodings': [array([-0.14319955,  0.06418357, ...)], 'names': ['Habib', 'Habib', ..., 'Tri Irfan', 'Tri Irfan']}

    cap = cv2.VideoCapture(0)
    nama = ""

    finis_time = datetime.datetime.now() + datetime.timedelta(seconds=5)

    while datetime.datetime.now() < finis_time:
        ret, frame = cap.read()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=400)
        r = frame.shape[1] / float(rgb.shape[1])
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(np.array(encoding), np.array(data["encodings"]))
            name = "Unknown"

            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    # print(i)
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
            names.append(name)
            nama = name

        for ((top, right, bottom, left), name) in zip(boxes, names):
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    print(nama)
    if nama != "" and nama != "Unknown":
        pass
    else:
        print("[INFO] Unknown Face, Please Try Again!!!")
        absents()

    with open('images/' + nama + '/data.txt', 'r') as file:
        data = json.load(file)

        for x in data['bio']:
            jsin = x
            jsonName = x['Name']
            jsonNIM = x['N I M']
            jsonClass = x['Class']

    print(jsin)
    print(jsonName)

    absName.set(jsonName)
    absNIM.set(jsonNIM)
    absClass.set(jsonClass)

    msgBox.showinfo(title="Success", message="Get data Successfully\nCheck your data correctly and make sure is that you!!")

    raise_frame(absentsPage)

"""=========================================== Confirm Absents Page ================================================="""
def sendData():
    getName = absName.get()
    getNIM = absNIM.get()
    getClass = absClass.get()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")

    print("Name : {}, N I M : {}, Class : {}, Date : {}, Arrival : {}".format(getName, getNIM, getClass, date, time))

    """======================================== SEND DATA INTO SERVER ==============================================="""
    # url = "http://localhost/presensi/absen.php"
    # payload = {'name': getName, 'nim': getNIM, 'class': getClass, 'date': date, 'time': time}
    # r = requests.post(url, data=payload)
    # print(r.text)

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

# Label(f3, text='FRAME 3').pack(side='left')
# Button(f3, text='Back to frame 1', command=lambda:raise_frame(f1)).pack(side='left')

Label(f4, text='FRAME 4').pack(side='right')
Button(f4, text='Back to frame 1', command=lambda:raise_frame(startPage)).pack(side='right')

raise_frame(startPage)


"""" ================================================ Main GUI ======================================================"""
signButton = Button(startPage, width=20, text="Sign Up", command=lambda:raise_frame(signPage))
signButton.grid(row=3, column=3, padx=5, pady=5)

absentButton = Button(startPage, width=20, text="Do Absent", command=absents)
absentButton.grid(row=5, column=0, padx=5, pady=5)


""""================================================= Train Data ===================================================="""
Label(signPage, text="Name  : ", bg=bg, fg=fg, font=font).grid(row=0, column=1, padx=5, pady=5)
Entry(signPage, width=30, textvariable=nameE).grid(row=0, column=2, padx=5, pady=5)

Label(signPage, text="N I M  : ", bg=bg, fg=fg, font=font).grid(row=1, column=1, padx=5, pady=5)
Entry(signPage, width=30, textvariable=nimE).grid(row=1, column=2, padx=5, pady=5)

Label(signPage, text="Class : ", bg=bg, fg=fg, font=font).grid(row=2, column=1, padx=5, pady=5)
# classEntry = Entry(signPage, width=30, textvariable=classE)
# classEntry.grid(row=2, column=2, padx=5, pady=5)
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
# birthEntry = Entry(signPage, width=30, textvariable=birthE)
# birthEntry.grid(row=3, column=2, padx=5, pady=5)

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
nameLabel = Label(absentsPage, text="Name  : ", bg=bg, fg=fg, font=font)
nameLabel.grid(row=0, column=1, padx=5, pady=5)

nameEntry = Entry(absentsPage, width=30, textvariable=absName)
nameEntry.grid(row=0, column=2, padx=5, pady=5)

nimLabel = Label(absentsPage, text="N I M  : ", bg=bg, fg=fg, font=font)
nimLabel.grid(row=1, column=1, padx=5, pady=5)

nimEntry = Entry(absentsPage, width=30, textvariable=absNIM)
nimEntry.grid(row=1, column=2, padx=5, pady=5)

classLabel = Label(absentsPage, text="Class : ", bg=bg, fg=fg, font=font)
classLabel.grid(row=2, column=1, padx=5, pady=5)

classEntry = Entry(absentsPage, width=30, textvariable=absClass)
classEntry.grid(row=2, column=2, padx=5, pady=5)

sendButton = Button(absentsPage, width=20, text="Confirm", command=sendData)
sendButton.grid(row=4, column=3, padx=5, pady=5)

backButton = Button(absentsPage, width=20, text="Try Again", command=absents)
backButton.grid(row=4, column=2, padx=5, pady=5)

root.mainloop()