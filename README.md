# PHYS265-spring24-lab1
# Nikhil Khosla
#Nikhil

# Code Project: 
# Once the Lmfit package is installed using 
pip install lmfit
# and updated using,
git clone https://github.com/lmfit/lmfit-py.git

# To reproduce Code Examples 1 & 2 found in the Code Project report:
# Example 1- H Beta Line
# One should first import all necessary python packages
import numpy as np
import matplotlib.pyplot as plt
import lmfit
from lmfit import Model
# Then, convert the given dataset into a readable txt file that can be read by numpy.loadtxt()
data = np.loadtxt('ngc253_hb.txt', encoding='utf-8-sig')
# Note that if you dont set encoding to utf-8, numpy will interpret the hidden
# text as a string and be unable to load the file

