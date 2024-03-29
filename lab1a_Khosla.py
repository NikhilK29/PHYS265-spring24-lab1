#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 12:19:05 2024

@author: nikhilkhosla
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from lab1a_utilities import calculate_force
from lab1a_utilities import calculate_potential
import lab1a_utilities as util

# Create the source charges
hidden_charges = np.array([[1,-100,-75],[-2.5,100,150],[1,-50,125]])


# Set the default initial conditions for v0, angle, and y0
v0, angle, y0 = 30.0, 55.066, -50.0     
 
# Keep x0 fixed at -100
x0 = -100.

def clear():
    
    # NO NEED TO EDIT THIS FUNCTION

    fig = plt.figure('Game Window')
    ax = fig.axes[0]
    ax.cla()
    ax.axis('square')
    ax.set_xlim(-200,200)
    ax.set_ylim(-200,200)
    ax.set_title('Electrostatic Projectile Game',fontsize=16)
    ax.set_xlabel('x position (meters)',fontsize=16)
    ax.set_ylabel('y position (meters)',fontsize=16)
    ax.grid(visible=True)
    fig.tight_layout()    
    fig.show()
    return
fig = plt.figure('Game Window')
ax = fig.add_subplot()
clear()


############################################################

def play():

    # NO NEED TO EDIT THIS FUNCTION

    global v0, angle, y0
    
    print("Starting x location is -100")
    v0 = float(input("Enter the initial speed between zero and 100.\n"))
    assert(v0 >= 0 and v0 <= 100), "Initial velocity should > 0 and < 100"
    angle = float(input("Enter the initial angle in degrees.\n"))
    assert(angle >= -180.00 and angle <= 180.00), \
        "Angle should be between -180 and +180"
    y0 = float(input("Enter the initial y position.\n"))
    assert(y0 >= -200 and y0 <= 200), "y0 should be between -200 and +200"
    
    plot_trajectory()
    
    return
 


############################################################

def reveal_potential():

    fig = plt.figure('Game Window')
    # for a 3D wireframe or surface plot, comment out this line:
    ax = fig.axes[0]
# Uncomment these lines to create a 3D wireframe or surface plot
    #fig.clf()
    #ax = fig.add_subplot(projection='3d')

    xx = np.linspace(-200,200,101)
    yy = np.linspace(-200,200,101)
    X,Y = np.meshgrid(xx,yy)
    Z = np.zeros((len(xx),len(yy)))
    for i in range(len(xx)):
        for j in range(len(yy)):
            x = X[i,j]
            y = Y[i,j]
            Z[i, j] = calculate_potential(x,y,hidden_charges)
    ax.contour(X,Y,Z,levels=[-7800,-7500,-7200,-6750,-6000,-5000,-4000,-3000,-2000,-1000,0\
                              ,1000,2000,2500,3000,3500,4000,4500,4750,5000,5300,5660,6000\
                                 ,6500,7000]) 
    return

############################################################

def reveal_forcefield():
    fig = plt.figure('Game Window')
    ax = fig.axes[0]
    
    # your code goes here


    return

############################################################


############################################################

def plot_trajectory():

    fig = plt.figure('Game Window')
    ax = fig.axes[0]
           
    def derivatives(t, s):
        #s[0] = x
        #s[1] = vx
        #s[2] = y
        #s[3] =vy
        #D[0] = vx
        #D[1]  = ax
        #D[2] = vy
        #D[3]  = ay
        Fx, Fy = calculate_force(s[0], s[2], hidden_charges)
        D = np.zeros(4)
        D[0] = s[1]
        D[1] = Fx
        D[2] = s[3]
        D[3] = Fy
        return D
    vx0 = v0*np.cos(angle)
    vy0 = v0*np.sin(angle)
    t0,tf = 0,10
    tt = np.linspace(t0,tf,101)
    vx0vals = np.arange(-5,5,1)


    for vx0 in vx0vals:
        solution = solve_ivp(derivatives,(t0, tf), [x0, vx0, y0, vy0], t_eval=tt)
        xx = solution.y[0]
        yy = solution.y[2]
        ax.plot(xx,yy,c='k')
        ax.plot(xx[::5],yy[::5],'oc',markersize=4)
        fig.show()

    return

############################################################

def solve_it():
    
    q1 = int(input('In quadrant 1, is there a: (1)Positive charge, (2)Negative, (3)Neither, or \
                      (4)Both?\n'))
    if q1 in [1,2,3,4]:
        if q1 == [1,3,4]:
            print('Incorrect! The charge in the first quadrant is negative.')
        else:
            print('Correct!')
    else:
        print('That is not a valid guess. Choose between 1, 2, 3, or 4.')
    q2 = int(input('\nIn quadrant 2, is there a: (1)Positive charge, (2)Negative, (3)Neither, or \
                      (4)Both?\n'))
    if q2 in [1,2,3,4]:
        if q2 == [2,3,4]:
            print('Incorrect! The charge in the second quadrant is positive.')
        else:
            print('Correct!')
    q3 = int(input('\nIn quadrant 3, is there: (1)Positive charge, (2)Negative, (3)Neither, or \
                      (4)Both?\nNote: it may prove useful to look at the origin of the trajectories\n'))
    if q3 in [1,2,3,4]:
        if q3 == [2,3,4]:
            print('Incorrect! The charge in the third quadrant is positive.')
        else:
            print('Correct!')
    q4 = int(input('\nIn quadrant 3, is there: (1)Positive charge, (2)Negative, (3)Neither, or \
                      (4)Both?\n'))
    if q4 in [1,2,3,4]:
        if q3 == [1,2,4]:
            print('Incorrect! There is no charge in the fourth quadrant.')
        else:
            print('Correct!')
    if q1 == 2 and q2 == 1 and q3 == 1 and q4 == 3:
        print('Congratulations! You got all questions correct and won the game!!')
        print('The hidden charge pontentials have been revealed!')
        reveal_potential()
        
    return
#%%
