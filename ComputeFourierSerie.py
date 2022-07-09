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


def g(t, Time, X, Y):
    '''Complex Representation of points defined by x_table and y_table during the time_table period in the complex plane at time t'''
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
    r_cn = np.array([quad(to_integrate_R, 0, 1, args=(n, Time, X, Y), limit=100, full_output=1)[0] for n in range(-N, N+1)])
    i_cn = np.array([quad(to_integrate_I, 0, 1, args=(n, Time, X, Y), limit=100, full_output=1)[0] for n in range(-N, N+1)])
    cn = np.concatenate((r_cn, i_cn)).reshape(2,r_cn.shape[0]).T
    return cn

def compute_fourier_serie_terms(cn, t, N):
    g_N = (cn[:,0]+1j*cn[:,1])*np.array([np.exp(1j*2*np.pi*n*t) for n in range(-N, N+1)])
    return g_N