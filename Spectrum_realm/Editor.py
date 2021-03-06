import numpy
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
import Parser
from Gaussian import Fitting
from PIL import Image, ImageTk
import os
import time
import functools
global Parsers

Parsers = {
    "Standard Parser, (.xyd, csv)" : Parser.Parser,
    "None" : None
}

def Find(key = "Standard Parser, (.xyd, csv)"):
    global Data
    Path = filedialog.askopenfilename()
    try:
        #Data = Fitting(Parser.Parser(Path))
        Data = Fitting(Parsers[key](Path))
    except Exception as e:
        messagebox.showwarning("Error", message="Loading data failed.")
        raise e
    HandlerProgram.Data = Data
    HandlerProgram.View()



def Progress(func):
    """A wrapper function that creates a progressbar during the call of the function, and then removes it."""
    def wrapper(*args, **kwargs):
        bar = ttk.Progressbar(master = root, length = 100, mode = 'indeterminate')
        bar.grid(column = 1, row = 11)
        bar.start()
        time.sleep(2)
        result = func(*args, **kwargs)
        try:
            time.sleep(2)
            bar.stop()
            bar.destroy()
        except:
            pass
        return result
    return wrapper

class Handler:
    Data = None
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x600")
        self.root.title("Spectrum Realm")
        Menubar = tk.Menu(root)
        self.Parser = "Standard Parser, (.xyd, csv)"
        Filemenu = tk.Menu(Menubar)
        Filemenu.add_command(label = "Parser : "+self.Parser, command = lambda : ChooseParser(self.root))
        Filemenu.add_command(label = "Load file", command = lambda: Find(self.Parser))
        Filemenu.add_command(label = "Manual fit", command = self.Manual)
        Filemenu.add_command(label = "Save figure", command = lambda : SaveFigure(self.root, self.Data))
        Menubar.add_cascade(label = "File", menu = Filemenu)
        BackgroundMenu = tk.Menu(Menubar)
        BackgroundMenu.add_checkbutton(label = "No Background")
        BackgroundMenu.add_checkbutton(label = "Exponential Background", command = self.Exp)
        BackgroundMenu.add_checkbutton(label = "Linear background", command = self.Lin)
        Menubar.add_cascade(label = "Background", menu = BackgroundMenu)
        Formatmenu = tk.Menu(Filemenu)
        Formatmenu.add_command(label = "Format", command = lambda: FormatHandler(self.root, self.Data))
        self.XrayTrue = tk.StringVar()
        Formatmenu.add_checkbutton(label = "Xray diffract", variable = self.XrayTrue, command = lambda : 0)
        Menubar.add_cascade(label = "Format", menu = Formatmenu)
        self.root.config(menu = Menubar)


        Label1 = ttk.Label(self.root, text = "Number of peaks").grid(column = 1, row = 1)
        self.NumberOfGaussiansval = tk.StringVar()
        self.NumberOfGaussiansval.set(1)
        self.NumberOfGaussians = ttk.Spinbox(self.root, from_ = 1, to = 20, textvariable = self.NumberOfGaussiansval,
            command = self.Update).grid(column = 1, row = 3)
        self.Boundaryval = tk.StringVar()
        self.Boundaryval.set(25)
        Label2 = ttk.Label(self.root, text = "Number of points to include").grid(column = 1, row = 5)
        self.Boundary = ttk.Spinbox(self.root, from_ = 15, to = 100, textvariable = self.Boundaryval,
            command = self.Update).grid(column = 1, row = 7)
        Btn1 = ttk.Button(root, text = "Apply", command = self.Update).grid(column = 1, row = 9)

    def Exp(self):
        try:
            self.Data.BackgroundCal(self.Data.Backgroundfunc["Exponential"])
            self.View()
        except Exception as e:
            raise e
    def Lin(self):
        try:
            self.Data.BackgroundCal(self.Data.Backgroundfunc["Linear"])
            self.View()
        except Exception as e:
            raise e

    #@Progress
    def Update(self):
        if self.Data == None:
            messagebox.showwarning("Error", f"Needs a file")
        else:
            try:
                self.Data.NumberOfFits = int(self.NumberOfGaussiansval.get())
                self.Data.Boundary = int(self.Boundaryval.get())
                self.Data.AutoDetectPeaks()
                text1 = tk.Text(master = self.root, height = 30, width = 50)
                text1.grid(column = 3, row = 1,rowspan = 9)
                scrollb = ttk.Scrollbar(master = self.root, command=text1.yview)
                scrollb.grid(column = 4, row=2, rowspan = 9, sticky='nsew')
                text1['yscrollcommand'] = scrollb.set
                text1.grid(column = 3, row=2, rowspan = 9)
                try:
                    if int(self.XrayTrue.get()) == 1:
                        try:
                            del self.Data.Miller
                        except:
                            pass
                        val = simpledialog.askfloat(title = "Assuming cubic structure", prompt = "Value in nm", initialvalue = 1)
                        self.Data.Compute(a = val)
                    else:
                        try:
                            del self.Data.Miller
                        except:
                            pass
                except:
                    pass
                text1.insert(tk.INSERT, self.Data.Data())
                self.View()
            except Exception as e:
                raise e

    def Manual(self):
        if Data == None:
            messagebox.showwarning("Error", message="Needs data.")
        else:
            Level = tk.Toplevel(master = self.root)
            Level.geometry("800x600")
            ManualFits(Level, self.Data)

    def View(self):
        try:
            self.Data.PlotFits()
            load1 = Image.open(os.path.join(os.getcwd(),"Current.png"))
            render1 = ImageTk.PhotoImage(load1)
            img1 = tk.Label(self.root, image = render1)
            img1.image = render1
            img1.grid(column = 2, row = 1, rowspan = 9)
        except Exception as e:
            raise e

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
        self.Update1()

    def Update1(self, value = None):
        index = int(self.Scale1val.get())
        boundary = int(self.Scale2val.get())
        try:
            self.Data.ManualInput(index, boundary)
            load2 = Image.open(os.path.join(os.getcwd(),"Manual.png"))
            render2 = ImageTk.PhotoImage(load2)
            img2 = tk.Label(self.master, image = render2)
            img2.image = render2
            img2.grid(column = 3, row = 1, rowspan = 4)
        except Exception as e:
            raise e

    def Commit(self):
        index = int(self.Scale1val.get())
        boundary = int(self.Scale2val.get())
        try:
            self.Data.Manual(index, boundary)
        except Exception as e:
            raise e

class FormatHandler(tk.Toplevel):
    def __init__(self, master, Data = None):
        super().__init__(master = master)
        self.master = master
        if Data == None:
            self.destroy()
            messagebox.showerror("Error", "Needs data to aquire")
        else:
            self.Data = Data
            xlabel = ttk.Label(master = self, text = "x-label").grid(column = 1, row = 1)
            ylabel = ttk.Label(master = self, text = "y-label").grid(column = 1, row = 2)
            title = ttk.Label(master = self, text = "Title").grid(column = 1, row = 3)
            self.XEntry = ttk.Entry(master = self)
            self.XEntry.grid(column = 2, row = 1)
            self.YEntry = ttk.Entry(master = self)
            self.YEntry.grid(column = 2, row = 2)
            self.TEntry = ttk.Entry(master =  self)
            self.TEntry.grid(column = 2, row = 3)
            btn = tk.Button(master = self, text = "Apply", command = self.Apply2).grid(column = 1, columnspan=2, row = 4)

    def Apply2(self):
        try:
            self.Data.xlabel = self.XEntry.get()
            self.Data.ylabel = self.YEntry.get()
            self.Data.Title = self.TEntry.get()
            HandlerProgram.View()
            self.destroy()
        except Exception as e:
            raise e

class SaveFigure(tk.Toplevel):
    def __init__(self, master, Data):
        super().__init__(master = master)
        self.Data = Data
        lbl = ttk.Label(master = self, text = "Name of spectrum").grid(column = 1, row = 1)
        self.master = master
        self.Name = ttk.Entry(master = self)
        self.Name.grid(column = 1, row = 2)
        btn = ttk.Button(master = self, text = "Save", command = self.save).grid(column =2, row = 1, rowspan = 2)
        if Data == None:
            self.destroy()
            messagebox.showerror("Error", "Needs a figure to save")

    def save(self):
        Path = Data.PathCurrent
        Path2 = Data.PathManual
        SavePath = filedialog.askdirectory()
        try:
            try:
                os.rename(Path, os.path.join(SavePath, self.Name.get()))
            except:
                messagebox.showerror("Error", "Could not save with that name")
            try:
                os.remove(Path)
            except:
                pass
            try:
                os.remove(Path2)
            except:
                pass
            self.destroy()
        except Exception as e:
            raise e

class ChooseParser(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master = master)
        self.master = master
        for item in (Parsers.items()):
            print(item)



if __name__ == '__main__':
    global root, HandlerProgram
    Data = None
    root = tk.Tk()
    HandlerProgram = Handler(root)
    root.mainloop()
