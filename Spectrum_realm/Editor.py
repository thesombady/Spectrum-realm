import numpy
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import Parser
from Gaussian import Fitting
from PIL import Image, ImageTk
import os
def Find():
    global Data
    Path = filedialog.askopenfilename()
    Data = Parser.Parser(Path)
    Handler.Data = Fitting(Data)


class Handler:
    Data = None
    def __init__(self, root):
        self.root = root
        Label1 = ttk.Label(self.root, text = "Number of peaks").grid(column = 1, row=1)
        self.NumberOfGaussiansval = tk.StringVar()
        self.NumberOfGaussiansval.set(1)
        self.NumberOfGaussians = ttk.Spinbox(self.root, from_ = 1, to = 20, textvariable = self.NumberOfGaussiansval,
            command = self.Update).grid(column = 1, row = 2)
        self.Boundaryval = tk.StringVar()
        self.Boundaryval.set(25)
        Label2 = ttk.Label(self.root, text = "Number of points to include").grid(column = 1, row = 3)
        self.Boundary = ttk.Spinbox(self.root, from_ = 25, to = 100, textvariable = self.Boundaryval,
            command = self.Update).grid(column = 1, row = 4)
        Btn1 = ttk.Button(root, text = "Apply", command = self.Update).grid(column = 1, row = 5)

    @classmethod
    def Settings(cls, root):
        root.geometry("1400x800")
        root.title("Spectrum Realm")
        Menubar = tk.Menu(root)
        Filemenu = tk.Menu(Menubar)
        Filemenu.add_command(label = "Load file", command = Find)
        Menubar.add_cascade(label = "File", menu = Filemenu)
        root.config(menu = Menubar)

    def Update(self):
        if self.Data == None:
            messagebox.showwarning("Error", f"Needs a file")
        else:
            try:
                self.Data.NumberOfFits = int(self.NumberOfGaussiansval.get())
                self.Data.Boundary = int(self.Boundaryval.get())
                self.Data.AutoDetectPeaks()
                self.Data.PlotFits()
            except Exception as e:
                raise e
            self.View()

    def View(self):
        load1 = Image.open(os.path.join(os.getcwd(),"Orignal.png"))
        render1 = ImageTk.PhotoImage(load1)
        img1 = tk.Label(self.root, image = render1)
        img1.image = render1
        img1.grid(column = 2, row = 1)
        try:
            load2 = Image.open(os.path.join(os.getcwd(),"Current.png"))
            render2 = ImageTk.PhotoImage(load2)
            img2 = tk.Label(self.root, image = render2)
            img2.image = render2
            img2.grid(column = 3, row = 1)
        except:
            pass





if __name__ == '__main__':
    global root
    Data = None
    root = tk.Tk()
    Handler.Settings(root)
    Handler(root)
    root.mainloop()
