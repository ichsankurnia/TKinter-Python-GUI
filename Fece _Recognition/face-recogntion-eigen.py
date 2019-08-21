from tkinter import *
import json
import tkinter as tk
from tkinter import messagebox as msgBox
import os
import cv2
import numpy as np
import pickle
import time
import datetime

def raise_frame(frame):
    frame.tkraise()

def saveData():
    name = nameE.get()
    nim = nimE.get()
    kelas = classE.get()
    # print(name + "\n" + nim + "\n" + kelas)

    os.mkdir('images/' + name)

    """Write Data JSON"""
    data = {}
    data['bio'] = [
        {"Name": name, "N I M": nim, "Class": kelas},
    ]

    with open('images/' + name + '/data.txt', 'w') as file:
        json.dump(data, file)

    msgBox.showinfo(title="Success", message="Save data successfully")
    msgBox.showwarning(title="Attention", message="Take Your Photo!!!")

    face_cascade = cv2.CascadeClassifier('face-detect.xml')
    cam = cv2.VideoCapture(0)

    id = 0
    while True:
        _, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        if cv2.waitKey(1) == 32:  # tombol spasi
            cv2.imwrite("images/" + name + "/" + str(id) + ".jpg", frame)
            print("Successed capturing image {}_{}".format(name, id))
            id += 1

        cv2.imshow('Press *Space button to capture', frame)

        if id > 9:
            print("Capture finish!!!")
            print('Please Wait.!!! Untill the mechine successed learning your face matrix')
            time.sleep(5)
            break

    cam.release()
    cv2.destroyAllWindows()

    msgBox.showinfo(title="Success", message="All your data has been saved")
    msgBox.showwarning(title="Attention", message="Please wait a moment")

    recognizer = cv2.face.EigenFaceRecognizer_create()

    current_id = 1
    label_ids = {}
    y_labels = []
    x_train = []

    BASE_DIR = os.path.dirname(__file__)
    image_dir = os.path.join(BASE_DIR, "images")

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('jpg') or file.endswith('JPG') or file.endswith('png'):
                path = os.path.join(root, file)
                label = os.path.basename(root).replace(' ', '-').lower()

                # berikan nomor id pada tiap label sesuai urutannya
                if not label in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]
                print(label_ids)

                # pil_image = Image.open(path)
                img = cv2.imread(path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.equalizeHist(img)
                # image_array = np.array(img, 'uint8')
                # x_train.append(img)
                # y_labels.append(id_)
                # size = (550, 550)
                # final_image = pil_image.resize(size, Image.ANTIALIAS)
                # image_array = np.array(final_image, 'uint8')  # bentuk matrix / NUMPY array image dengan numpy
                # # print(image_array) # np array tiap gambar
                face = face_cascade.detectMultiScale(img, 1.3, 5)
                for x, y, w, h in face:
                    roi = img[y:y + h, x:x + w]  # wajah atau objek yg di deteksi wajah dalam matrix
                    x_train.append(cv2.resize(roi, (280, 280)))  # tambahkan roi pada list x_train
                    y_labels.append(
                        id_)  # berikan id pada objek wajah yg di deteksi berdasakan nama labelnya (nama label = nama folde gambar orang ex:ichsan)
                    # print(x_train)

    with open('pickle/fixxx.pickle', 'wb') as f:  # labels_ids = nama folder orang, buat pake pickle 'wb'
        pickle.dump(label_ids, f)  # buat file .pickle untuk label

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save('train/fixxx.yml')

    print('Trainning Success')
    msgBox.showinfo(title="Success", message="All your data has been trained")

    raise_frame(startPage)

def absents():
    recognizer = cv2.face.EigenFaceRecognizer_create()
    recognizer.read('train/fixxx.yml')

    labels = {'person-name': 1}
    with open('pickle/fixxx.pickle', 'rb') as f:  # open file pickle yg berisi label orang
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}  # value : key  dari 'person-name' : 1 =>>> 1 : 'person-name'

    jsonName = ''
    jsonNIM = ''
    jsonClass = ''
    mhs = ''
    jsin = {}
    # iden = []

    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('face-detect.xml')

    finis_time = datetime.datetime.now() + datetime.timedelta(seconds=5)

    while datetime.datetime.now() < finis_time:
        _, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(img, 1.3, 5)  # scaleFactor=1.5, minNeighbors = 5

        if len(faces) > 0:
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                roi_gray = img[y:y + h, x:x + w]

                # recognizer
                id_, conf = recognizer.predict(cv2.resize(roi_gray, (280, 280)))
                if conf >= 45:
                    print(id_)
                    print(labels[id_])
                    cv2.putText(frame, 'Nama = ' + str(labels[int(id_)]).replace('-', ' '), (10, 465),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(frame, 'ID : ' + str(id_), (10, 435), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                                cv2.LINE_AA)
                    mhs = labels[id_].replace('-', '_')

                    with open('images/' + str(labels[int(id_)]).replace('-', ' ') + '/data.txt', 'r') as file:
                        data = json.load(file)

                        for x in data['bio']:
                            jsin = x
                            jsonName = x['Name']
                            jsonNIM = x['N I M']
                            jsonClass = x['Class']
        else:
            print("Face is not recognize")

        cv2.imshow('press *R to back to main menu', frame)

        if cv2.waitKey(1) & 0xFF == ord('r'):
            break

    absName.set(jsonName)
    absNIM.set(jsonNIM)
    absClass.set(jsonClass)

    print(jsonName)  # Ichsan Kurniawan
    print(mhs)  # ichsan_kurniawan
    print(jsin)  # {'Name': 'Ichsan Kurniawan', 'N I M': '136010006', 'Class': 'EC_6B'}
    print(jsin['Name'])  # Ichsan Kurniawan

    # url = "http://localhost/test/in.php"
    # payload = {'test': 'ichsan_kurniawan'}
    # r = requests.post(url, data=payload)
    # print(r.text)  # Success Table : ichsan_kurniawan

    # time.sleep(3)
    cam.release()
    cv2.destroyAllWindows()

    msgBox.showinfo(title="Success", message="Get data Successfully\nCheck your data correctly and make sure is that you!!")

    raise_frame(absentsPage)


def sendData():
    raise_frame(startPage)


root = Tk()

root.title("Test")
root.resizable(width=False, height=False)
root.config(bg="black")
# root.geometry(newGeometry="590x575")

startPage = Frame(root, bg="black") # , width=100, height=100
signPage = Frame(root, bg="black")
absentsPage = Frame(root, bg="black")
f4 = Frame(root, bg="black")

nameE = StringVar()
nimE = StringVar()
classE = StringVar()

absName = StringVar()
absNIM = StringVar()
absClass = StringVar()


"""" ================================================ Main GUI ======================================================"""
signButton = Button(startPage, width=20, text="Sign Up", command=lambda:raise_frame(signPage))
signButton.grid(row=3, column=3, padx=5, pady=5)

absentButton = Button(startPage, width=20, text="Do Absent", command=absents)
absentButton.grid(row=5, column=0, padx=5, pady=5)


""""================================================= Train Data ===================================================="""
font = ('Helvetica', 10)
bg = "black"
fg = "white"

nameLabel = Label(signPage, text="Name  : ", bg=bg, fg=fg, font=font)
nameLabel.grid(row=0, column=1, padx=5, pady=5)

nameEntry = Entry(signPage, width=30, textvariable=nameE)
nameEntry.grid(row=0, column=2, padx=5, pady=5)

nimLabel = Label(signPage, text="N I M  : ", bg=bg, fg=fg, font=font)
nimLabel.grid(row=1, column=1, padx=5, pady=5)

nimEntry = Entry(signPage, width=30, textvariable=nimE)
nimEntry.grid(row=1, column=2, padx=5, pady=5)

classLabel = Label(signPage, text="Class : ", bg=bg, fg=fg, font=font)
classLabel.grid(row=2, column=1, padx=5, pady=5)

classEntry = Entry(signPage, width=30, textvariable=classE)
classEntry.grid(row=2, column=2, padx=5, pady=5)

saveButton = Button(signPage, width=20, text="Save", command=saveData)
saveButton.grid(row=4, column=3, padx=5, pady=5)

backButton = Button(signPage, width=20, text="Back", command=lambda:raise_frame(startPage))
backButton.grid(row=4, column=2, padx=5, pady=5)


"""================================================ Absents ========================================================="""
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


"""=================================================================================================================="""
for frame in (startPage, signPage, absentsPage, f4):
    frame.grid(row=0, column=0,sticky='news')

# Label(f3, text='FRAME 3').pack(side='left')
# Button(f3, text='Back to frame 1', command=lambda:raise_frame(f1)).pack(side='left')

Label(f4, text='FRAME 4').pack(side='right')
Button(f4, text='Back to frame 1', command=lambda:raise_frame(startPage)).pack(side='right')

raise_frame(startPage)

root.mainloop()