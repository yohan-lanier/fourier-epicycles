'''
@author : yohan lanier
@date : 06/07/2022
@brief : 
resources on fourier series and fourier transform : 
	+ https://www.jezzamon.com/fourier/index.html 
	+ https://www.youtube.com/watch?v=r6sGWTCMz2k&list=RDCMUCYO_jab_esuFRV4b17AJtAw&index=3
    + https://en.wikipedia.org/wiki/Fourier_series
    + https://www.youtube.com/watch?v=spUNpyF58BY&list=RDCMUCYO_jab_esuFRV4b17AJtAw&index=1
    + https://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/ 
    + https://alex.miller.im/posts/fourier-series-spinning-circles-visualization/ 
'''

import numpy as np
from scipy.integrate import quad 
from tqdm import tqdm

def g(t, Time, X, Y):
    '''
    Complex Representation of points defined by X and Y during the Time period in the complex plane at time t
    ---------------------------------------------------------------------------------------------------------

    Inputs :
    ---------------------------------------------------------------------------------------------------------

        + t : float
            Value of the time t at which X and Y has to be evaluated using the interp method of numpy
        + Time : numpy array, shape = X.shape
            Array containing time values on which to X and Y tables are defined. Used for the interpolation
        + X/Y : numpy arrays
            Arrays defining a function on the interval of time defined by the table Time. These functions are the ones to be interpolated
        

    Output :
    ---------------------------------------------------------------------------------------------------------
        
        + X+Y : complex value
            The interpolated value of the function X+jY at the time t
    '''
    #using numpy interpolation function : for each time t of the table t, np.interp get the value 
    # of the linear interpolated function of time table and x_table 
    X = np.interp(t, Time, X) 
    #Same as above for Y + creation of the complex variable Z
    Y = 1j*np.interp(t, Time, Y)
    return X + Y

def to_integrate_R(t, n, Time, X, Y):
    to_integrate = g(t, Time, X, Y)*np.exp(-1j*2*np.pi*n*t)
    return np.real(to_integrate)

def to_integrate_I(t, n, Time, X, Y):
    to_integrate = g(t, Time, X, Y)*np.exp(-1j*2*np.pi*n*t)
    return np.imag(to_integrate)

def compute_cn(Time, X, Y, N):
    '''
    Method used to compute all Cn coefficients of the Fourier sum of order N of the function defined by X+jY during Time. Complex exponential formulation is used. @warning : the convention being used is that the function X+jY is defined on the intervalof time [0,1]
    ---------------------------------------------------------------------------------------------------------
    
    Inputs : 
    ---------------------------------------------------------------------------------------------------------
        + Time : 1D nupy array
                By convention defined as np.linspace(0,1, X.shape[0])
        + X/Y : 1D numpy arrays
                These arrays represent the X and Y coordinates of the drawing one is trying to animate.
        + N : integer
                Order of of the fourier sum. The sum will range from -N, to N, hence 2*N+1 coefficients

    Outputs :
    ---------------------------------------------------------------------------------------------------------
    
        + cn : numpy array, shape = (2*N+1, 2)
            array containing all cn coefficients of the Fourier sum representing the function X+jY. First column is the real part of the coeffs, second one is the imag one.
    '''
    print('\nComputing real components of cn coefficients\n')
    r_cn = np.array([quad(to_integrate_R, 0, 1, args=(n, Time, X, Y), limit=100, full_output=1)[0] for n in tqdm(range(-N, N+1))])
    print('\nComputing imag components of cn coefficients\n')
    i_cn = np.array([quad(to_integrate_I, 0, 1, args=(n, Time, X, Y), limit=100, full_output=1)[0] for n in tqdm(range(-N, N+1))])
    cn = np.concatenate((r_cn, i_cn)).reshape(2,r_cn.shape[0]).T
    return cn

def compute_fourier_serie_terms(cn, t, N):
    '''
    Compute the terms of the fourier serie of order N at time t using the complex exponential formulation
    ---------------------------------------------------------------------------------------------------------

    Inputs : 
    ---------------------------------------------------------------------------------------------------------
        + cn : numpy array, shape = (2*N+1, 2)
            array containing all cn coefficients of the Fourier sum representing the function X+jY. First column is the real part of the coeffs, second one is the imag one.
        + t : float 
            Time at which the fourier serie terms are computed
        + N : integer
                Order of of the fourier sum. The sum will range from -N, to N, hence 2*N+1 coefficients

    Outputs : 
    ---------------------------------------------------------------------------------------------------------
        + g_N : 1D numpy array, shape = cn.shape[0]
            An array containing the 2*N+1 terms of the Fourier sum of order N approximating the function g evaluated at time t

    '''
    g_N = (cn[:,0]+1j*cn[:,1])*np.array([np.exp(1j*2*np.pi*n*t) for n in range(-N, N+1)])
    return g_N