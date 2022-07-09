from ReadSvgPath import *
from ComputeFourierSerie import *
from Visualize import *
import sys
import numpy as np

def plot_points(points):
    plt.plot(points[:,0], points[:,1], '+-')
    plt.show()

if __name__ == '__main__':

    filename = sys.argv[-1]
    N = 40
    path_list = extract_paths_from_svg_file(filename)
    points = read_svg_path_and_return_XY_tab(path_list[0], n_points=500)
    plot_points(points)

    points = format_list_of_points(points)
    fig_lims = compute_fig_lims(points)
    Time = np.linspace(0, 1, points.shape[0])# as I have taken the convention of defining the function between 0 and 1 in the fourier notations
    X = points[:,0]
    Y = points[:,1]
    cn = compute_cn(Time, X, Y, N)
    SerieCoef = np.array([compute_fourier_serie_terms(cn, t, N) for t in Time]).T
    anim = visualize(SerieCoef, N, fig_lims)
    plt.show()

