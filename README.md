# Spectrum realm
A spectrum analyzer program that is written in python, utilizing Tkinter as graphical user interface. A simple userface of which allows for automatic detection of peaks in an emission/diffraction spectrum using a rather primitive maximum algorithm. With options like, background fitting, different parsers and different experiment requests, one can use this program to analyse spectrums from experiments in physics and chemistry in undergrad studies.

# Method
The maximum algorithm works upon the basis of always finding new maximums in the dataset. This sadly restricts the program; The peaks lower than the maximum of the trend, will not be detected. This is avoided by simply adding a manual input. Moreover, this is not the fastest method but yields adequate results

# Undergoing
As mentioned above, the program is not the fastest and this is currently being looked into. A faster method, utilizing "concurrent.futures" will be implemented when it's thoroughly tested. Moreover, more parsing methods will be implemented. Lastly, different experiment requests will also be implemented, such that the relevant information will be provided.
