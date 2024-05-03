# PHYS265-spring24-CODE-PROJECT
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

# Then, convert the given dataset into a readable txt file that can be read by numpy.loadtxt() and interpret the data as columns
data = np.loadtxt('ngc253_hb.txt', encoding='utf-8-sig')

x = data[:, 0]
y = data[:, 1]

# Note that if you dont set encoding to utf-8, numpy will interpret the hidden text as a string and be unable to load the file
# Next define the Gaussian function being used:

def hbeta(x,a,b,c,d):
    return a+b*np.exp(-(x-c)**2/(2*d**2))

# Create a reasonable uncertainty by examining the data. Next, assign the Lmfit Model function to a variable and then use the make_params function of the variable to get your parameters
uncertainty = 100.0
gaussmodel = Model(hbeta)
params = gaussmodel.make_params(a=np.mean(y),b=np.max(y)-np.min(y),c=np.mean(x),d=np.std(x))

# Next, assign your result to using the .fit function with the previously found parameters in order to store all the necessary elements of the dataset
res = gaussmodel.fit(y,params,x=x,weights=1.0/uncertainty)
# Note that weights gives the uncertainties and can affect the chi-squared value

# Next to print the data and make the plots of the fit and dataset, you can use 
print(res.fit_report())
# and
plt.plot(x,res.init_fit,'--',label='initial fit')
plt.plot(x,res.best_fit,'-',label='best fit')
# for the initial and best fit curves 
# Dont forget to plot the data points
plt.plot(x,y,'o')
plt.title('Lmfit')
plt.legend()

# This should print out the full report of the data set and the fit, along with plotting dataset, fit line, and initial fit line


# Example 2-- Two dimensional peaks fit



