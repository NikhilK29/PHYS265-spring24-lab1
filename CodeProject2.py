#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:47:30 2024

@author: nikhilkhosla
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

import lmfit
from lmfit.lineshapes import gaussian2d, lorentzian

npoints = 10000
np.random.seed(3142)
x = np.random.rand(npoints)*10 - 2
y = np.random.rand(npoints)*5 - 3
z = gaussian2d(x,y,amplitude=18,centerx=4,centery=0,sigmax=0.75,sigmay=.6)
z += 2*(np.random.rand(*z.shape)-0.5)
error = np.sqrt(z+1)

X, Y = np.meshgrid(np.linspace(x.min(),x.max(),100),np.linspace(y.min(),y.max(),100))
Z = griddata((x,y),z,(X,Y),method='linear',fill_value=0)

fig,ax = plt.subplots()
art = ax.pcolor(X,Y,Z,shading='auto')
plt.colorbar(art,ax=ax,label='z')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

#%%

model = lmfit.models.Gaussian2dModel()
params = model.guess(z,x,y)
result = model.fit(z,x=x,y=y,params=params,weights=1/error)
lmfit.report_fit(result)


fig,axs = plt.subplots(2,2,figsize=(10,10))
vmax = np.nanpercentile(Z,99.9)

ax = axs[0,0]
art = ax.pcolor(X,Y,Z,vmin=0, vmax=vmax,shading='auto')
plt.colorbar(art,ax=ax,label='z')
ax.set_title('Data')

ax = axs[0,1]
fit = model.func(X,Y,**result.best_values)
art = ax.pcolor(X,Y,fit,vmin=0,vmax=vmax,shading='auto')
plt.colorbar(art,ax=ax,label='z')
ax.set_title('Fit')

ax = axs[1,0]
fit = model.func(X,Y,**result.best_values)
art = ax.pcolor(X,Y,Z-fit,vmin=0,vmax=10,shading='auto')
plt.colorbar(art,ax=ax,label='z')
ax.set_title('Data - Fit')

for ax in axs.ravel():
    ax.set_xlabel('x')
    ax.set_ylabel('y')
axs[1,1].remove()
plt.show()
plt.tight_layout()