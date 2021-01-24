import numpy as np
from scipy.optimize import curve_fit


def Linear(x,y):
    """A linear regression on the form of 'y = k*x+m'. Utalizes scipy.optimize.curve_fit."""
    if not isinstance((x,y), (np.generic, np.ndarray)):
        if isinstance((x,y), (list, tuple)):
            x = np.array(x); y = np.array(y)
        else:
            raise ValueError("[Linear]: Needs a iterable as input")
    if len(x) != len(y):
        raise ValueError("[Linear]: The length of x and y are not equal.")
    lin = lambda x, k,m: k*x+m
    try:
        func, covarience = curve_fit(lin, x,y)
        return func, covarience, (lambda x: func[0]*x+ func[2])
    except Exception as e:
        raise e

def Exponential(x,y):
    """A exponential regression on the form 'y = Ce^(-x/k)'. Utalizes scipy.optimize.curve_fit."""
    if not isinstance((x,y), (np.generic, np.ndarray)):
        if isinstance((x,y), (list, tuple)):
            x = np.array(x); y = np.array(y)
        else:
            raise ValueError("[Exponential]: Needs a iterable as input")
    if len(x) != len(y):
        raise ValueError("[Exponential]: The length of x and y are not equal.")
    expo = lambda x, C,a, k, b: C*a**(-x/k) + b
    try:
        func, covarience = curve_fit(expo, x,y)
        print(func)
        return lambda x: func[0]*func[1]**(-x/func[2]) + func[3]#,func, covarience
    except:
        try:
            for i in range(1,len(x)):
                if x[i-1]<x[i]:
                    x[i] = x[i-1]
            func, covarience = curve_fit(expo, x,y)
            return lambda x: func[0]*func[1]**(-x/func[2])+ func[3]#, func, covarience
        except Exception as e:
            raise e
