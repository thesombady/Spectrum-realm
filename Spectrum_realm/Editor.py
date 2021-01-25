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
    try:
        Data = Fitting(Parser.Parser(Path))
    except:
        messagebox.showwarning("Error", message="Loading data failed.")
    Handler.Data = Data


class Handler:
    Data = None
    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x800")
        self.root.title("Spectrum Realm")
        Menubar = tk.Menu(root)
        Filemenu = tk.Menu(Menubar)
        Filemenu.add_command(label = "Load file", command = Find)
        Filemenu.add_command(label = "Manual fit", command = self.Manual)
        Menubar.add_cascade(label = "File", menu = Filemenu)
        self.root.config(menu = Menubar)



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
        self.ViewData = tk.Text(master = self.root, height = 5, width = 10).grid(column = 2, row = 2)
        #self.Scrollbar = tk.Scrollbar(master = self.root).grid(column = 2, row = 2)
        #self.Scrollbar.config(command = self.ViewData.yview)
        #self.Viewdata.config(yscrollcommand=self.Scrollbar.set)


    def Update(self):
        if self.Data == None:
            messagebox.showwarning("Error", f"Needs a file")
        else:
            try:
                self.Data.NumberOfFits = int(self.NumberOfGaussiansval.get())
                self.Data.Boundary = int(self.Boundaryval.get())
                self.Data.AutoDetectPeaks()
                self.Data.PlotFits()
                #self.ViewData.delete('1.0', tk.END)
                #self.ViewData.insert(tk.END, self.Data.Data())
            except Exception as e:
                raise e
            self.View()

    def Manual(self):
        if Data == None:
            messagebox.showwarning("Error", message="Needs data.")
        else:
            Level = tk.Toplevel(master = self.root)
            Level.geometry("600x500")
            ManualFits(Level, self.Data)

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

class ManualFits():
    def __init__(self, root, Data):
        self.master = root
        if Data == None:
            raise TypeError("")
        self.Data = Data
        self.Scale2val = tk.DoubleVar()
        self.Scale2 = ttk.Scale(master = self.master, from_ = 20, to = 50, variable = self.Scale2val,
            command = self.Update1).grid(column = 1, row = 2)
        label2 = ttk.Label(master = self.master, text = "Boundary").grid(column = 2, row =2)
        self.Scale1val = tk.DoubleVar()
        self.Scale1 = ttk.Scale(master = self.master, from_ = 0, to = len(self.Data.x) - int(self.Scale2val.get() + 1),
            variable = self.Scale1val,
            command = self.Update1).grid(column = 1, row = 1)
        label1 = ttk.Label(master = self.master, text = "Index").grid(column = 2, row = 1)
        self.Scale1val.set(1)
        self.Scale2val.set(25)
        Btn1 = ttk.Button(master = self.master, text = "Apply fit", command = self.Commit).grid(column = 1, row = 3)

    def Update1(self, value = None):
        index = int(self.Scale1val.get())
        boundary = int(self.Scale2val.get())
        try:
            self.Data.ManualInput(index, boundary)
            load2 = Image.open(os.path.join(os.getcwd(),"Manual.png"))
            render2 = ImageTk.PhotoImage(load2)
            img2 = tk.Label(self.master, image = render2)
            img2.image = render2
            img2.grid(column = 3, row = 4)
        except Exception as e:
            raise e

    def Commit(self):
        index = int(self.Scale1val.get())
        boundary = int(self.Scale2val.get())
        try:
            self.Data.Manual(index, boundary)
        except Exception as e:
            raise e



if __name__ == '__main__':
    global root
    Data = None
    root = tk.Tk()
    Handler(root)
    root.mainloop()
