import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


NB_OF_SPACE_REPEATS = 1
SPACE = 1000
NB_OF_DRAG = 500

def center_list_of_values(L):
    L = L - min(np.absolute(L))-max(np.absolute(L))/2
    return L

def format_list_of_points(points):
    points[:,0] = center_list_of_values(points[:,0])
    #flip image to match matplotlib coordinate system
    points[:,1] = -1*center_list_of_values(points[:,1])
    return points

def compute_fig_lims(points):
    fig_lims = [max(np.absolute(points[:,0])*1.5), max(np.absolute(points[:,1])*1.5)]
    return fig_lims

def create_circle_around_center(center, radius):
    theta = np.linspace(0, 2*np.pi, 50)
    X, Y = radius * np.cos(theta) + center.real, radius * np.sin(theta) + center.imag
    return X, Y

def visualize(Fourier_serie_terms, N, fig_lims):

    #fig settings
    fig, ax = plt.subplots(facecolor = 'black')
    plt.style.use('dark_background')
    fig.set_facecolor('black')
    fig.tight_layout()
    ax.set_frame_on(False)
    ax.set_facecolor('black')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    print(fig_lims)
    lim = max(fig_lims)
    print(lim)
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
    ax.set_aspect('equal')
    ax.set_facecolor('black')

    g_N = np.sum(Fourier_serie_terms, axis=0)#Fourier serie terms for all time t of the interval of Time

    line = plt.plot([], [], '-', color = (255/255, 0/255, 0/255), linewidth=3)[0]
    Vectors = plt.plot([], [], 'o-', color = (0/255, 255/255, 255/255), linewidth=1, markersize = 3)[0]
    Circles = [plt.plot([], [], '-', color = (0/255, 255/255, 255/255), linewidth=0.5)[0] for _ in range(2*N+1)]
    
    def animate(i):
        g_i = g_N[:i]
        line.set_data(g_i.real, g_i.imag)
        vectors = list(Fourier_serie_terms[:,i])
        vectors.sort(key=lambda z: np.absolute(z), reverse = True) 
        amplitudes = np.absolute(vectors)
        cumulated_vectors = np.array([np.sum(vectors[:k+1]) for k in range(len(vectors))])
        cumulated_vectors = np.concatenate((np.zeros((1,)),cumulated_vectors))
        Vectors.set_data(cumulated_vectors.real, cumulated_vectors.imag)
        for k, circle in enumerate(Circles) :
            X,Y = create_circle_around_center(cumulated_vectors[k], amplitudes[k])
            circle.set_data(X, Y)
    
    ani = animation.FuncAnimation(fig, animate, frames=NB_OF_SPACE_REPEATS*g_N.shape[0], interval=10)
    return ani