from ReadSvgPath import *
from ComputeFourierSerie import *
from Visualize import *
import sys
import numpy as np

def plot_points(points):
    plt.plot(points[:,0], points[:,1], '+-')
    plt.show()

def main():
    if len(sys.argv) == 3:
        file = sys.argv[-2]
        N = int(sys.argv[-1])
    elif len(sys.argv) == 2 : 
        N = 10
        file = sys.argv[-1]
    else : 
        print('invalid number of arguments')

    if file.split('.')[-1] == 'svg':
        path_list = extract_paths_from_svg_file(file)
        n_paths = len(path_list)
        print(f'{n_paths} svg paths detected, only the first one will be processed \n')
        print('chose number of points for the discretization of the svg path. Please enter an integer number. 500 is a good basis\n')
        n_points = int(input())
        points = read_svg_path_and_return_XY_tab(path_list[0], n_points=500)
        #format the list of points from svg coordinate system to matplotlib coordinate system
        points = format_list_of_points(points)
        #plot the detected path for pre-visualization
        plot_points(points)
        fig_lims = compute_fig_lims(points)
        Time = np.linspace(0, 1, points.shape[0])# as I have taken the convention of defining the function between 0 and 1 in the fourier notations
        X = points[:,0]
        Y = points[:,1]
        #Compute the cn coefficient of the Fourier serie
        cn = compute_cn(Time, X, Y, N)
        #Compute the serie coefficient for all time t in table T
        print('\nComputing serie coefficients for all times t\n')
        SerieCoef = np.array([compute_fourier_serie_terms(cn, t, N) for t in tqdm(Time)]).T
        #Create the animation
        anim = visualize(SerieCoef, N, fig_lims)
        plt.show()

if __name__ == '__main__':
    main()

