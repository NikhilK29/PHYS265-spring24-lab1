# PHYS265-spring24-CODE-PROJECT
# Nikhil Khosla

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
<img width="397" alt="Screenshot 2024-05-02 at 9 48 56 PM" src="https://github.com/NikhilK29/PHYS265-spring24-lab1/assets/163023737/bc1115fa-3dd1-4ae4-a843-f809011079da">
<img width="572" alt="Screenshot 2024-05-02 at 10 43 19 PM" src="https://github.com/NikhilK29/PHYS265-spring24-lab1/assets/163023737/b4c05c82-4854-449f-bf6c-38da48b012e6">



# Example 2-- Two dimensional peaks fit

# For creating 2D peaks fit, the following must be done
# Import all necessary python packages: 

    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.interpolate import griddata
    import lmfit
    from lmfit.lineshapes import gaussian2d, lorentzian
# Next, we must create a simple 2 dimensional Gaussian function with reasonable noise and random sampling by making use of gaussian2d
    npoints = 10000
    np.random.seed(3142)
    x = np.random.rand(npoints)*10 - 2
    y = np.random.rand(npoints)*5 - 3
    z = gaussian2d(x,y,amplitude=18,centerx=4,centery=0,sigmax=0.75,sigmay=.6)
    z += 2*(np.random.rand(*z.shape)-0.5)
    error = np.sqrt(z+1)
# Note that if desiring to reproduce the same results, the random seed 3142 has been added so that it should look the same as yours
# Next we must plot this onto a grid, using colorbar in order to highligh where the peaks of the data exist
    X, Y = np.meshgrid(np.linspace(x.min(),x.max(),100),np.linspace(y.min(),y.max(),100))
    Z = griddata((x,y),z,(X,Y),method='linear',fill_value=0)
    
    fig,ax = plt.subplots()
    art = ax.pcolor(X,Y,Z,shading='auto')
    plt.colorbar(art,ax=ax,label='z')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
# Now our first plot of the randomized dataset is shown including the noise
<img width="549" alt="Screenshot 2024-05-02 at 10 10 05 PM" src="https://github.com/NikhilK29/PHYS265-spring24-lab1/assets/163023737/ace27783-a377-4ede-a955-be3b5c2679df">

# Next, in order to make and print the fit of the dataset we must use models, guess, fit, and report_fit
    model = lmfit.models.Gaussian2dModel()
    params = model.guess(z, x, y)
    result = model.fit(z, x=x, y=y, params=params, weights=1/error)
    lmfit.report_fit(result)
# This should result in getting the chi-squared, number of data points, R-squared, variables, and correlations
<img width="566" alt="Screenshot 2024-05-02 at 10 57 01 PM" src="https://github.com/NikhilK29/PHYS265-spring24-lab1/assets/163023737/9d6093da-da03-40a4-886a-f1d6cd7ff4c3">

# Now to just plot the fitted two-dimensional peak we must simply use the best_values function of lmfit
# It would also be useful to create plots side by side showing the non-fitted, fitted, and difference between them to check the effectivity of the package
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    vmax = np.nanpercentile(Z, 99.9)
    
    ax = axs[0, 0]
    art = ax.pcolor(X, Y, Z, vmin=0, vmax=vmax, shading='auto')
    plt.colorbar(art, ax=ax, label='z')
    ax.set_title('Data')
    
    ax = axs[0, 1]
    fit = model.func(X, Y, **result.best_values)
    art = ax.pcolor(X, Y, fit, vmin=0, vmax=vmax, shading='auto')
    plt.colorbar(art, ax=ax, label='z')
    ax.set_title('Fit')
    
    ax = axs[1, 0]
    fit = model.func(X, Y, **result.best_values)
    art = ax.pcolor(X, Y, Z-fit, vmin=0, vmax=10, shading='auto')
    plt.colorbar(art, ax=ax, label='z')
    ax.set_title('Data - Fit')
# This should provide our side-by-side comparisons showing how truly effective lmfit's fitting has been in a two dimensional setting
<img width="984" alt="Screenshot 2024-05-02 at 10 15 17 PM" src="https://github.com/NikhilK29/PHYS265-spring24-lab1/assets/163023737/ae0e9724-f631-4984-bbf8-1246e1ef7c83">



