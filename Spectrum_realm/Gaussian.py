from Background import Exponential, Linear
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

class Fitting:
    def __init__(self, Data):
        if not isinstance((Data[0],Data[1]), (np.generic, np.ndarray)):
            if isinstance((Data[0],Data[1]), (list, tuple)):
                self.x = np.array(Data[0]); self.y = np.array(Data[1])
            else:
                raise ValueError("[Fitting]: Can't create instance")
        self.Background = None
        self.Title = " "
        self.xlabel = " "
        self.ylabel = " "
        self.NumberOfFits = 4
        self.FitsMade = []
        self.Boundary = 25

    def PlotData(self):
        plt.plot(self.x,self.y, '.', markersize=2)
        plt.title(self.Title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.show()

    def Manual(self, index1, index2):
        pass

    def AutoDetectPeaks(self):
        XVal = self.x.copy()
        YVal = self.y.copy()
        gauss = lambda x, a, mu, sigma: a*np.exp(-(x - mu)**2/(2*sigma**2))
        bd = self.Boundary
        dlist = np.linspace(self.x[0], self.x[-1], len(self.x)*10)
        for i in range(self.NumberOfFits):
            maximum = max(YVal)
            index = int(np.where(YVal == maximum)[0])
            Xlist = XVal[index-bd:index +bd]
            Ylist = YVal[index-bd:index +bd]
            try:
                mean = sum(Xlist * Ylist)/sum(Ylist)
                guesssigma = np.sqrt(sum(Ylist * (Xlist - mean)**2) / sum(Ylist))
                Fit, covarience = curve_fit(gauss, Xlist, Ylist, p0 = [max(Ylist), mean, guesssigma])
                func = lambda x: Fit[0]*np.exp(-(x-Fit[1])**2/(2*Fit[2]**2))
                #self.FitsMade.append(func)
                print(Fit)
                #print(covarience)
            except Exception as e:
                raise e
            xlist = list(XVal); ylist = list(YVal)
            del xlist[index-bd: index + bd]; del ylist[index-bd: index + bd]
            XVal = np.array(xlist); YVal = np.array(ylist)
            ylist = func(dlist)
            self.FitsMade.append((dlist, ylist))

    def BackgroundCal(self, func):
        if not callable(func):
            raise TypeError("[Fitting.Background] Requires a function as input")
        else:
            fit = func(self.x, self.y)
        xlist = np.linspace(self.x[0], self.x[-1], len(self.x)*10)
        ylist = fit(xlist)
        self.Background = ylist

    def PlotFits(self):
        plt.plot(self.x, self.y, '.', markersize = 1, label = "Data")
        for i in range(len(self.FitsMade)):
            if not isinstance(self.Background, (np.ndarray, np.generic)):
                Background = 0
            else:
                Background = self.Background
            plt.plot(self.FitsMade[i][0], self.FitsMade[i][1] + Background, '-', label = f"Fit to peak {i+1}")
            print(max(self.FitsMade[i][1]))
        plt.legend()
        plt.grid()
        plt.show()




def Parser(Path):
    """Parser function provides the parsered data provided from a .xyd file. This method requires that the data
    is strictly ordered"""
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
        return np.array(Xlist), np.array(Ylist)
    except:
        raise Exception("[Parser]: Cant find the input")


a = Fitting(Parser(os.path.join("/Users/andreasevensen/Desktop/Uni/Semester4/XrayDiffraction", "AG.xyd")))
a.Title = "Test"
a.AutoDetectPeaks()
a.BackgroundCal(Exponential)
a.PlotFits()
#a.PlotData()
