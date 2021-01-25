from Background import Exponential, Linear
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from PhysicsNum import RiemanSum

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
        self.NumberOfFits = 1
        self.FitsMade = []
        self.ManualFits = []
        self.ManualError =  []
        self.ManualArea = []
        self.Error = []
        self.Area = []
        self.Boundary = 25
        self.PlotData()

    def PlotData(self):
        plt.plot(self.x,self.y, '.', markersize=2)
        plt.title(self.Title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.savefig("Orignal.png")
        plt.clf()

    def Manual(self, index, boundary):
        xlist = self.x[index - boundary:index + boundary]; ylist = self.y[index - boundary:index + boundary]
        gauss = lambda x, a, mu, sigma: a*np.exp(-(x - mu)**2/(2*sigma**2))
        try:
            mean = sum(xlist * ylist)/sum(ylist)
            guesssigma = np.sqrt(sum(ylist * (xlist - mean)**2) / sum(ylist))
            Fit, covarience = curve_fit(gauss, xlist, ylist, p0 = [max(ylist), mean, guesssigma])
            func = lambda x: Fit[0]*np.exp(-(x-Fit[1])**2/(2*Fit[2]**2))
        except Exception as e:
            raise e
        dlist = np.linspace(self.x[0],self.x[-1], len(self.x)*10)
        self.ManualFits.append(dlist, func(np.linspace(self.x[0],self.x[-1], len(self.x)*10)))

    def ManualInput(self, index, boundary, commit = False):
        plt.plot(self.x, self.y, '.', markersize = 0.8, label = "Data")

        plg.grid()
        plt.legend()
        plt.title(self.Title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.savefig("Manual.png")
        plt.cfg()
        if commit == True:
            self.Manual(index, boundary)

    def AutoDetectPeaks(self):
        del self.FitsMade
        del self.Error
        del self.Area
        self.Error = []
        self.Area = []
        self.FitsMade = []
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
            except Exception as e:
                raise e
            xlist = list(XVal); ylist = list(YVal)
            del xlist[index-bd: index + bd]; del ylist[index-bd: index + bd]
            XVal = np.array(xlist); YVal = np.array(ylist)
            ylist = func(dlist)
            self.FitsMade.append((dlist, ylist))
            self.Error.append(covarience)
            self.Area.append(RiemanSum(func, self.x[0], self.x[-1]))

    def BackgroundCal(self, func):
        if not callable(func):
            raise TypeError("[Fitting.Background] Requires a function as input")
        else:
            fit = func(self.x, self.y)
        xlist = np.linspace(self.x[0], self.x[-1], len(self.x)*10)
        ylist = fit(xlist)
        self.Background = ylist

    def PlotFits(self):
        if len(self.FitsMade) != 0:
            plt.plot(self.x, self.y, '.', markersize = 1, label = "Data")
            for i in range(len(self.FitsMade)):
                if not isinstance(self.Background, (np.ndarray, np.generic)):
                    Background = 0
                else:
                    Background = self.Background
                plt.plot(self.FitsMade[i][0], self.FitsMade[i][1] + Background, '-', label = f"Fit to peak {i+1}")
                #print(max(self.FitsMade[i][1]))
            plt.legend()
            plt.grid()
            plt.savefig("Current.png")
            plt.clf()
        else:
            pass
