import tkinter as tk
from tkinter import *
from tkinter.messagebox import *

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="Home").grid(row=0,column=1, padx=10, pady=10)
        Button(self, text="Absent",
                  command=lambda: master.switch_frame(PageAbsent)).grid(row=3, column=3, padx=5, pady=5)
        Button(self, text="Sign Up",
                  command=lambda: master.switch_frame(PageSign)).grid(row=5, column=0, padx=5, pady=5)

class PageAbsent(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        font = ('Helvetica', 10)
        bg = "black"
        fg = "white"

        self.nameE=StringVar()
        self.nimE = StringVar()
        self.classE = StringVar()

        nameLabel = Label(self, text="Name  : ", bg=bg, fg=fg, font=font)
        nameLabel.grid(row=0, column=1, padx=5, pady=5)

        nameEntry = Entry(self, width=30, textvariable=self.nameE)
        nameEntry.grid(row=0, column=2, padx=5, pady=5)

        nimLabel = Label(self, text="N I M  : ", bg=bg, fg=fg, font=font)
        nimLabel.grid(row=1, column=1, padx=5, pady=5)

        nimEntry = Entry(self, width=30, textvariable=self.nimE)
        nimEntry.grid(row=1, column=2, padx=5, pady=5)

        classLabel = Label(self, text="Class : ", bg=bg, fg=fg, font=font)
        classLabel.grid(row=2, column=1, padx=5, pady=5)

        classEntry = Entry(self, width=30, textvariable=self.classE)
        classEntry.grid(row=2, column=2, padx=5, pady=5)
        Button(self, text="Return to start page",
                  command=self.savedata).grid(row=4, column=3, padx=5, pady=5)

    def savedata(self):

        name = self.nameE.get()
        nim = self.nimE.get()
        kelas = self.classE.get()

        print(name, nim, kelas)
        showinfo(title="Success", message="Save data successfully")

        self.quit()

        SampleApp()

class PageSign(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()