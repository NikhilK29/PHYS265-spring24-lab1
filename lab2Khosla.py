#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:04:41 2024

@author: nikhilkhosla
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from scipy.optimize import curve_fit

fig = plt.figure(1,figsize=(6,6))
fig.clf()
axes = [fig.add_subplot(321),\
        fig.add_subplot(322),\
        fig.add_subplot(323),\
        fig.add_subplot(324),\
        fig.add_subplot(325),\
        fig.add_subplot(326)]

# You can use axes[0], axes[1], ....  axes[5] to make the six histograms.



data = np.loadtxt("refractionData.txt",skiprows=3)

for i in range(6):
    axes[i].hist(data[i],bins=5)
    axes[i].set_title(f"alpha = {i*10+10} deg.")
    axes[i].set_xlim([-10,50])
    axes[i].set_xticks(np.arange(-10,50.1,10))
    axes[i].set_xlabel("beta(deg.)")
    axes[i].set_ylim(auto=True)
    
plt.tight_layout()

#%%

# Part 2 - Table of measurements
betamean = np.mean(np.radians(data),axis=1)
betasin = np.sin(betamean)
betastd = np.std(np.radians(data),axis=1)  
uncsinbeta = betasin*betastd

print("a\t\tSin(a)\t\tB\t\tSin(B)\t\tSin_err(Beta)")
print("-----------------------------------------------------")
for i in range(6):
    print(f"{i*10+10}\t\t{np.sin(np.radians(i*10+10)):.3f}\t\t{betamean[i]:.3f}\t\t{betasin[i]:.3f}\t\t{uncsinbeta[i]:.3f}")

#%%

# Part 3 - Snells law plot and fit


fig = plt.figure(2,figsize=(6,6))
fig.clf()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)


alpha = np.arange(10,61,10)
alphasin = np.sin(np.radians(alpha))

def snellslaw(alphasin,n):
    return np.sin(np.arcsin(alphasin)/n) # for b

params,covar = curve_fit(snellslaw,alphasin,betasin)
err = np.sqrt(covar[0][0])

alphasinfit = np.linspace(0,1,100) #from 0-90 degrees
betasinfit = snellslaw(alphasinfit,params[0])
chisq = np.sum((betasin-snellslaw(alphasin,params[0]))**2)
pvalue = st.chi2.sf(chisq,len(betasin)-1)

print("Best Fit Value of Index of Refraction (n): {:.3f} ± {:.2f}".format(params[0],err))
print("Chi-squared: {:.7f}".format(chisq))
print("Degrees of Freedom: 5")
print("p-value: {:.12f}".format(pvalue))

ax1.errorbar(alphasin,betasin,yerr=uncsinbeta,fmt='o',label='Data points')
ax1.plot(alphasinfit,betasinfit,label=f'Curve fit: n={params[0]:.2f}±{err:.2f}')
ax1.set_xlabel('sin(a)')
ax1.set_ylabel('sin(B)')
ax1.set_title('Sin(B) vs Sin(a)')
ax1.grid()
ax1.legend()



# Part 4 - Chi squared plot


nvals = np.linspace(1.55,1.65,100) 
chisqvals = np.zeros(len(nvals))
for i in range(len(nvals)):
    expectedbetasin = snellslaw(alphasin,nvals[i])
    chisqvals[i] = np.sum((betasin - expectedbetasin)**2)

chisqmin = chisqvals[0]
for i in range(len(chisqvals)):
    if chisqvals[i] < chisqmin:
        chisqmin = chisqvals[i]
        minlinevalue = i
         
chi_squared_sigma = chisqmin + uncsinbeta[2]**2
ax2.plot(nvals,chisqvals,label='Chi Squared vs n')
#vert and horizontal lines
ax2.axvline(x=nvals[minlinevalue],c='k',linestyle='--',label='Minimum chisq')
ax2.axvline(x=nvals[minlinevalue] - uncsinbeta[4],c='r',linestyle='--',label='n-1sig')
ax2.axvline(x=nvals[minlinevalue] + uncsinbeta[4],c='b',linestyle='--',label='n+1sig')
ax2.axhline(y=chisqmin,c='g',linestyle='--',label='Minimum chisq')
ax2.axhline(y=chi_squared_sigma,c='m',linestyle='--',label='Minimum chisq+1sig')
ax2.set_xlabel('Index of Refraction(n)')
ax2.set_ylabel('Chi Squared')
ax2.set_title('Chi Squared vs Index of Refraction')
ax2.set_ylim(min(chisqvals)-0.0001,max(chisqvals)+0.0001)
ax2.legend()
plt.tight_layout()











######################################################