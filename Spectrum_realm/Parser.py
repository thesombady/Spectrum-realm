import os
import numpy as np
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
