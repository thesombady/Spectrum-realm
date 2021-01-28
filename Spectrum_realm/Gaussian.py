#from Background import Exponential, Linear
import Background
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from PhysicsNum import RiemanSum
import time
import math

class Fitting:

    Backgroundfunc ={"Exponential" : Background.Exponential,
        "Linear" : Background.Linear}

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
        self.FitsMadeVal = []
        self.ManualFits = []
        self.ManualFitsVal = []
        self.ManualError =  []
        self.ManualArea = []
        self.Error = []
        self.Area = []
        self.Boundary = 25
        self.PlotData()
        self.PathCurrent = os.path.join(os.getcwd(), "Current.png")
        self.PathManual = os.path.join(os.getcwd(), "Manual.png")

    def PlotData(self):
        plt.plot(self.x,self.y, '.', markersize=2)
        plt.title(self.Title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.savefig("Current.png")
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
        self.ManualFits.append((dlist, func(np.linspace(self.x[0],self.x[-1], len(self.x)*10))))
        self.ManualFitsVal.append((Fit[0], Fit[1], Fit[2]))
        self.ManualError.append(covarience)
        self.ManualArea.append(RiemanSum(func, self.x[0], self.x[-1]))

    def ManualInput(self, index, boundary = 25):
        plt.plot(self.x, self.y, '.', markersize = 0.8, label = "Data")
        plt.axvline(self.x[index - boundary])
        plt.axvline(self.x[index + boundary])
        plt.grid()
        plt.legend()
        plt.title(self.Title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.savefig("Manual.png")
        plt.clf()


    def AutoDetectPeaks(self):
        del self.FitsMade
        del self.Error
        del self.Area
        del self.FitsMadeVal
        self.Error = []
        self.Area = []
        self.FitsMade = []
        self.FitsMadeVal = []
        XVal = self.x.copy()
        YVal = self.y.copy()
        gauss = lambda x, a, mu, sigma: a*np.exp(-(x - mu)**2/(2*sigma**2))
        bd = self.Boundary
        dlist = np.linspace(self.x[0], self.x[-1], len(self.x)*10)
        for i in range(self.NumberOfFits):
            maximum = max(YVal)
            try:
                index = int(np.where(YVal == maximum)[0])
            except:
                break
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
            self.FitsMadeVal.append((Fit[0], Fit[1], Fit[2]))

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
        if len(self.FitsMade) != 0:
            for i in range(len(self.FitsMade)):
                if not isinstance(self.Background, (np.ndarray, np.generic)):
                    Background = 0
                else:
                    Background = self.Background
                plt.plot(self.FitsMade[i][0], self.FitsMade[i][1] + Background, '-', label = f"Fit to peak {i+1}")
        if len(self.ManualFits) != 0:
            for i in range(len(self.ManualFits)):
                if not isinstance(self.Background, (np.ndarray, np.generic)):
                    Background = 0
                else:
                    Background = self.Background
                plt.plot(self.ManualFits[i][0], self.ManualFits[i][1] + Background, label = f"Manual fits{i+1}")
        if isinstance(self.Background, (np.generic, np.ndarray)):
            plt.plot(np.linspace(self.x[0], self.x[-1], len(self.x)*10),
                self.Background,'-', label = "Background")
        plt.legend()
        plt.grid()
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.Title)
        plt.savefig("Current.png")
        plt.clf()

    def Data(self):
        text = " "
        for i in range(len(self.Error)):
            text += f"_______Automated peak {i+1}_______\n"
            text += f"Covarience {self.Error[i]}\n"
            text += f"Area  = {self.Area[i]}\n"
            text += f"Amplitude = {self.FitsMadeVal[i][0]}\nMu = {self.FitsMadeVal[i][1]}\nError = {self.FitsMadeVal[i][2]}\n\n "
        text += "\n\n\n"
        for i in range(len(self.ManualFits)):
            text += f"_______Manual peak {i+1}_______\n"
            text += f"Covarience {self.ManualError[i]} for manual peak {i+1}\n"
            text += f"Area = {self.ManualArea[i]}\n"
            text += f"Amplitude = {self.ManualFitsVal[i][0]}\nMu = {self.ManualFitsVal[i][1]}\nError = {self.ManualFitsVal[i][2]}\n\n"
        try:
            text += str(self.Miller)
        except Exception as e:
            print(e)
        return text

    def Compute(self, a = 1, b = None, c = None, alpha = 1, Beta = 1, gamma = 0, Accurarcy = 0.01, wavelength = 1.54):
        """Will compute if one says it's xray XRD-spectrum."""
        Distance = []#Distance between planes
        for i in range(len(self.FitsMadeVal)):
            val = math.radians(self.FitsMadeVal[i][1]/2)
            d = wavelength/(2*math.sin(val))
            Distance.append([d, self.FitsMadeVal[i][1]])
        for i in range(len(self.ManualFitsVal)):
            val = math.radians(self.ManualFitsVal[i][1]/2)
            d = wavelength/(2*math.sin(val))
            Distnce.append([d, self.ManualFitsVal[i][1]])
        Miller = {}
        if b == None or c == None:
            if b == None:
                b = a
            if c == None:
                c = a
            else:
                b, c = a, a
        for h in [0,1,2,3,4]:
            for k in [0,1,2,3,4]:
                for l in [0,1,2,3,4]:
                    for i in range(len(Distance)):
                        Difference = abs((1/Distance[i][0])**2 - ((h/a)**2 + (k/b)**2 + (l/c)**2))
                        if Difference < Accurarcy:
                            Miller[f'Peak at {Distance[i][1]}'] =  f"({h},{k},{l})"
        self.Miller = Miller
