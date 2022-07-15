from Exceptions import NoPathInSVG, test_a_color
from ReadSvgPath import *
from ComputeFourierSerie import *
from Visualize import *
import argparse
import numpy as np
import matplotlib
###############################################################
#WARNING : Change this path to the location of your writer
matplotlib.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\USERNAME\\anaconda3\\Library\\bin\\ffmpeg.exe'


def plot_points(points):
    plt.plot(points[:,0], points[:,1], '+-')
    plt.show()

def main(args):

    file = args['file']
    N = args['order']
    n_points = args['n_points']
    se = args['se']
    oo = args['oo']
    tail_color = args['tail_color']
    tail_color = test_a_color(tail_color)
    head_color = args['head_color']
    head_color = test_a_color(head_color)
    save_path = args['save_path']
    
    ext = file.split('.')[-1]
    if ext == 'svg':
        path_list = extract_paths_from_svg_file(file)
        n_paths = len(path_list)
        print('\n-------------------------------------')
        print(f'{n_paths} svg paths detected. If more than 1 only the first one will be processed')
        print('Discretizing svg path')
        print('-------------------------------------\n')
        try :
            if n_paths == 0:
                raise NoPathInSVG
        except NoPathInSVG as npis :
                print(npis)
                return
        points = read_svg_path_and_return_XY_tab(path_list[0], n_points=n_points)
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
        print('\n-------------------------------------')
        print('Computing serie coefficients for all times t')
        print('-------------------------------------\n')
        SerieCoef = np.array([compute_fourier_serie_terms(cn, t, N) for t in tqdm(Time)]).T
        #Create the animation
        mycolors = define_color_map(head_color, tail_color)
        anim = visualize(SerieCoef, N, fig_lims, mycolors, tail_color, head_color, Start_empty=se, Opacity_on=oo)
        if save_path != None :
            print('\n-------------------------------------')
            print('Saving the animation')
            print('-------------------------------------\n')
            save_path = r''+save_path
            writervideo = animation.FFMpegWriter(fps=30) 
            dpi=200
            anim.save(save_path, writer=writervideo, dpi=dpi, progress_callback = lambda i, n: print(f'Saving frame {i} of {n}'))
        plt.show()
    else : 
        print('\n-------------------------------------')
        print(f'This version only processes svg files. You passed in a {ext} which is not supported. Try again with an svg')
        print('-------------------------------------\n')


if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument('file', help ='String containing the path to the svg file')
    arguments.add_argument('-order', metavar = 'N', default = 10, type= int, help = 'Order to of Fourier sum, a value of N will result in 2*N+1 terms in the sum')
    arguments.add_argument('-n_points', default = 500, type = int, help = 'Number of points used to discretize the svg path')
    arguments.add_argument('-se', metavar = 'Start empty', default = False, help = 'A boolean used to determine if the animation starts with an empty drawing or not')
    arguments.add_argument('-oo', metavar = 'Opacity on', default = True, help = 'A boolean used to determine if an opacity effect is used in the animation')
    arguments.add_argument('-head_color', default = 'white', type = str, help = 'string representing the color of the head of the animation. A color gradient will be created between head and tail. Possible options are r, b, g, b, c, y, p, o, w. Default is w')
    arguments.add_argument('-tail_color', default = 'white', type = str, help = 'string representing the color of the tail of the animation. A color gradient will be created between head and tail. Possible options are r, b, g, b, c, y, p, o, w. Default is w')
    arguments.add_argument('-save_path', type = str, help = 'if used, the animation will be saved to the location indicated by this path under the name at the end of it. The path needs to end with video-name.mp4, It should look something like c://Users/user-name/Desktop/video.mp4. Gif format is also valid' )
    args = vars(arguments.parse_args())
    main(args)

