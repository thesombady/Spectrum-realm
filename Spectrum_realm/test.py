import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import os
import sys
import numpy as np
import math
import pandas as pd

FIG_SIZE = (10, 8)
PLOT_LIMIT = 12
TICK_INTERVAL = 1.5

def transform_point(point, angle):
        alpha = - angle/180 * math.pi
        x_t = point[0] * math.cos(alpha) - point[1] * math.cos(math.pi/2 - alpha)
        y_t = point[0] * math.sin(alpha) + point[1] * math.sin(math.pi/2 - alpha)
        return x_t, y_t

def Parser():
    global Xlist, Ylist
    Path = filedialog.askopenfilename()
    try:
        with open(Path, 'r') as file:
            Data = file.readlines()
        Xlist = []
        Ylist = []
        for i in range(len(Data)):
            Values = Data[i].split(' ')
            val2 = Values[-1].replace("\n", '')#Remove a newline and replace by nothing
            Xlist.append(float(Values[0]))
            Ylist.append(float(val2))
        #return np.array(Xlist), np.array(Ylist)
        Xlist = np.array(Xlist); Ylist = np.array(Ylist)
    except:
        raise Exception("[Parser]: Cant find the input")

class MplMap():
    @classmethod
    def settings(cls, root, fig_size, plot_limit):
        # set the plot outline, including axes going through the origin
        cls.fig, cls.ax = plt.subplots(figsize=fig_size)
        cls.plot_limit = plot_limit
        cls.ax.set_xlim(-cls.plot_limit, cls.plot_limit)
        cls.ax.set_ylim(-cls.plot_limit, cls.plot_limit)
        cls.ax.set_aspect(1)
        tick_range = np.arange(
            round(-cls.plot_limit + (10*cls.plot_limit % TICK_INTERVAL*10)/10, 1),
            cls.plot_limit + 0.1,
            step=TICK_INTERVAL)
        cls.ax.set_xticks(tick_range)
        cls.ax.set_yticks(tick_range)
        cls.ax.tick_params(axis='both', which='major', labelsize=6)
        cls.ax.spines['left'].set_position('zero')
        cls.ax.spines['right'].set_color('none')
        cls.ax.spines['bottom'].set_position('zero')
        cls.ax.spines['top'].set_color('none')
        cls.canvas = FigureCanvasTkAgg(cls.fig, master=root)

    @classmethod
    def get_canvas(cls):
        return cls.canvas

class Plotdata(MplMap):

    def __init__(self, *arg):
        self._facecolor = 'none'
        self._edgecolor = 'green'
        self._lw = 5
        self.alpha = 0
        c1 = (-1, +1)
        c2 = (-2, +4)
        c3 = (+2, +4)
        c4 = (+1, +1)
        self.Data = arg
        self.PlotData()

    def PlotData(self):
        self.clear_map()
        xlist = self.Data[0]
        ylist = self.Data[1]
        self.ax.fill(xlist, ylist,
                     fc=self._facecolor,
                     ec=self._edgecolor,
                     lw=self._lw)
        self.canvas.draw()

    def clear_map(self):
        for patch in self.ax.patches:
            patch.remove()

    def set_color(self, color):
        self._edgecolor = color
        self.plot_shape()

    def set_angle(self, alpha):
        self.alpha = alpha
        self.plot_shape()

    def set_line_width(self, width):
        self._lw = width/10
        self.plot_shape()


class PlotRectangle(MplMap):

    def __init__(self):
        self._facecolor = 'none'
        self._edgecolor = 'green'
        self._lw = 5
        self.alpha = 0
        c1 = (-1, +1)
        c2 = (-2, +4)
        c3 = (+2, +4)
        c4 = (+1, +1)
        self.a_shape = np.array([c1, c2, c3,])
        self.plot_shape()

    def plot_shape(self):
        self.clear_map()
        trsfd_shape = []
        for point in self.a_shape:
            trsfd_shape.append(transform_point(point, self.alpha))

        trsfd_shape = np.array(trsfd_shape)
        self.ax.fill(trsfd_shape[:, 0], trsfd_shape[:, 1],
                     fc=self._facecolor,
                     ec=self._edgecolor,
                     lw=self._lw)
        self.canvas.draw()

    def clear_map(self):
        for patch in self.ax.patches:
            patch.remove()

    def set_color(self, color):
        self._edgecolor = color
        self.plot_shape()

    def set_angle(self, alpha):
        self.alpha = alpha
        self.plot_shape()

    def set_line_width(self, width):
        self._lw = width/10
        self.plot_shape()


class Tk_Handler():

    def __init__(self, root, canvas, shape):
        self.root = root
        self.shape = shape

        self.root.wm_title("Embedding MPL in tkinter")
        sliders_frame = tk.Frame(self.root)
        slider_frame_1 = tk.Frame(sliders_frame)
        label_slider_1 = tk.Label(slider_frame_1, text='\nAngle: ')
        slider_1 = tk.Scale(slider_frame_1, from_=-180, to=180, orient=tk.HORIZONTAL,
                            command=lambda angle: self._tilt_shape(angle))
        slider_1.set(0)
        label_slider_1.pack(side=tk.LEFT)
        slider_1.pack(side=tk.LEFT)
        slider_frame_1.pack()

        slider_frame_2 = tk.Frame(sliders_frame)
        label_slider_2 = tk.Label(slider_frame_2, text='\nWidth: ')
        slider_2 = tk.Scale(slider_frame_2, from_=0, to=10, orient=tk.HORIZONTAL,
                            command=lambda width: self._lw_shape(width))
        slider_2.set(5)
        label_slider_2.pack(side=tk.LEFT)
        slider_2.pack(side=tk.LEFT)
        slider_frame_2.pack()

        button_frame = tk.Frame(self.root)
        quit_button = tk.Button(button_frame, text="Quit", command=self._quit)\
            .pack(side=tk.LEFT)
        green_button = tk.Button(button_frame, text="Green",\
            command=lambda *args: self._color_shape('green', *args))\
            .pack(side=tk.LEFT)
        red_button = tk.Button(button_frame, text="Red",\
            command=lambda *args: self._color_shape('red', *args))\
            .pack(side=tk.LEFT)

        # fill the grid
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        sliders_frame.grid(row=0, column=0, sticky=tk.NW)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=1, columnspan=1,
                                    sticky=tk.W+tk.E+tk.N+tk.S)

        tk.mainloop()

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                             # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _color_shape(self, color):
        self.shape.set_color(color)

    def _lw_shape(self, width):
        self.shape.set_line_width(float(width)*4)

    def _tilt_shape(self, angle):
        self.shape.set_angle(float(angle))



def main():
    root = tk.Tk()
    Menubar = tk.Menu(root)
    FileMenu = tk.Menu(Menubar)
    FileMenu.add_command(label = "Load file", command = Parser)
    Menubar.add_cascade(label = "File", menu = FileMenu)
    root.config(menu = Menubar)
    MplMap.settings(root, FIG_SIZE, PLOT_LIMIT)
    Tk_Handler(root, MplMap.get_canvas(), PlotRectangle())


if __name__ == "__main__":
    main()
