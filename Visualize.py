import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.collections import LineCollection
import matplotlib.colors as colors


NB_OF_SPACE_REPEATS = 1

def define_color_map(head_color, tail_color):
    fade = colors.to_rgb(tail_color) + (0.0,)
    mycolors = colors.LinearSegmentedColormap.from_list('my',[fade, head_color])
    return mycolors

def center_list_of_values(L):
    L = L - min(L)/2 - max(L)/2
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

def visualize(Fourier_serie_terms, N, fig_lims, mycolors, Start_empty = False, Opacity_on = True):
    #fig settings
    #------------------------------------------------
    fig, ax = plt.subplots(facecolor = 'black')
    plt.style.use('dark_background')
    fig.set_facecolor('black')
    fig.tight_layout()
    ax.set_frame_on(False)
    ax.set_facecolor('black')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    lim = max(fig_lims)
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    #------------------------------------------------
    #Fourier serie terms for all time t of the interval of Time
    g_N = np.sum(Fourier_serie_terms, axis=0)
    #Initialize plots
    #------------------------------------------------
    Vectors = plt.plot([], [], 'o-', color = (255/255, 255/255, 255/255), linewidth=1, markersize = 2)[0]
    Circles = [plt.plot([], [], '-', color = (255/255, 255/255, 255/255), linewidth=0.5, alpha=0.5)[0] for _ in range(2*N+1)]
    if Start_empty :
        if Opacity_on :
            #Normalize is used so that the set_array method can pass in an array containing numbers between 0 and 1
            lines = LineCollection([], cmap=mycolors, lw=2, norm=plt.Normalize(0,1))
            ax.add_collection(lines)
        else :
            line = plt.plot([], [], '-', color = (255/255, 0/255, 0/255), linewidth=2)[0]
    else :
            #if starting empty is turned to false, collection is initialized
            points = np.array([g_N.real, g_N.imag]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)   
            #the array argument is also initialized 
            alphas_fix_length = np.array([_/g_N.shape[0] for _ in range(g_N.shape[0])])
            #Normalize is used so that the set_array method can pass in an array containing numbers between 0 and 1
            lines = LineCollection(segments, array=alphas_fix_length ,cmap=mycolors, lw=2, norm=plt.Normalize(0,1))
            ax.add_collection(lines)
    #------------------------------------------------
    def animate(i):
        g_i = g_N[:i]
        if Start_empty :
            if Opacity_on :
                #Array used to map the colormap on the segments of the line collection
                alphas = np.array([_/i for _ in range(i)])
                #update array
                lines.set_array(alphas)
                points = np.array([g_i.real, g_i.imag]).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)   
                #Update of the plot         
                lines.set_segments(segments)
            else :
                #Update of the plot  
                line.set_data(g_i.real, g_i.imag)
        else : 
            #if drawing does not start empty, the opacity of the plot is the only thing to update
            if Opacity_on :
                alphas = alphas_fix_length.copy()
                alphas[:i+1] = alphas_fix_length[-(i+1):]
                alphas[i+1:] = alphas_fix_length[:-(i+1)]
                lines.set_array(alphas)
        #Sorting vectors using their amplitude
        vectors = list(Fourier_serie_terms[:,i])
        vectors.sort(key=lambda z: np.absolute(z), reverse = True) 
        amplitudes = np.absolute(vectors)
        #Computing the cumulated sum at time t
        cumulated_vectors = np.array([np.sum(vectors[:k+1]) for k in range(len(vectors))])
        cumulated_vectors = np.concatenate((np.zeros((1,)),cumulated_vectors))
        #Update vectors
        Vectors.set_data(cumulated_vectors.real, cumulated_vectors.imag)
        for k, circle in enumerate(Circles) :
            X,Y = create_circle_around_center(cumulated_vectors[k], amplitudes[k])
            #Update circles
            circle.set_data(X, Y)
    #set up animation    
    ani = animation.FuncAnimation(fig, animate, frames=NB_OF_SPACE_REPEATS*g_N.shape[0], interval=10)
    return ani