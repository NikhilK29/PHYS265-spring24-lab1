#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 12:28:29 2024

@author: nikhilkhosla
"""
import numpy as np
import matplotlib.pyplot as plt
import lmfit
from lmfit import Model

data = np.loadtxt('ngc253_hb.txt', skiprows=1, encoding='utf-8-sig')

x = data[:,0]
y = data[:,1]

def hbeta(x,a,b,c,d):
    return a+b*np.exp(-(x-c)**2/(2*d**2))

uncertainty = 100.0
gaussmodel = Model(hbeta)
params = gaussmodel.make_params(a=np.mean(y),b=np.max(y)-np.min(y),c=np.mean(x),d=np.std(x))
res = gaussmodel.fit(y,params,x=x,weights=1.0/uncertainty)

print("Using lmfit:")
print(res.fit_report())

plt.figure(1)
plt.plot(x,y,'o')
plt.plot(x,res.init_fit,'--',label='initial fit')
plt.plot(x,res.best_fit,'-',label='best fit')
plt.title('Lmfit')
plt.legend()
plt.show()

#%%
from scipy.optimize import curve_fit

data = np.loadtxt('ngc253_hb.txt',skiprows=1,encoding='utf-8-sig')
x = data[:,0]
y = data[:,1]

def hbeta(x,a,b,c,d):
    return a+b*np.exp(-(x-c)**2/(2*d**2))

parameters,covar = curve_fit(hbeta,x,y,p0=[np.mean(y),np.max(y)-np.min(y),np.mean(x),np.std(x)])

afit,bfit,cfit,dfit = parameters

print("-"*70)
print("Parameters using curve_fit:")
print("a =",afit)
print("b =",bfit)
print("c =",cfit)
print("d =",dfit)

plt.figure(2)
plt.plot(x,y,'o',label='data')
plt.plot(x,hbeta(x,*parameters),'-',label='fit')
plt.title('curve_fit')
plt.legend()
plt.show()
