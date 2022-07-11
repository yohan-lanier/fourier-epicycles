'''
@author : yohan lanier
@date : 06/07/2022
@brief : set of functions allowing to extract paths contained in an svg file using svg.path package
resources on svg files : 
	+ https://www.adobe.com/creativecloud/file-types/image/vector/svg-file.html
	+ https://alexvong.substack.com/p/the-code-behind-svgs 
	+ https://gjenkinsedu.com/post/drawing_py_svg_path_0001/
	+ https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Specific_cases
'''

from svg.path import parse_path
import numpy as np

def extract_paths_from_svg_file(filename):
	#initialize variable to count how many path there are in svg
	path_counter = 0
	#initialize list to store path
	path_list =[] #list of strings
	#boolean to indicate wether or not a path has entirely been detected
	in_path = False
	with open(filename, 'r') as f :
		for line in f :
			#clear line
			line = line.strip()
			#detect path begining
			if line[:5] == '<path':
				path_counter+=1
				#search for variable d in the path
				for _ in range(5, len(line)):
					if line[_]+line[_+1]=='d=':
						break
				#append the path to the list
				path_list.append(line[_+3:])
				in_path = True
			elif in_path == False :
				pass
			else : 
				l = len(line)
				#detect end of line
				if line[l-2:] == '/>' :
					path_list[path_counter-1]+=line[:l-3]
					#exit path
					in_path = False
				else :
					path_list[path_counter-1]+=line
	return path_list


def read_svg_path_and_return_XY_tab(svg_path, n_points=100):
	path = parse_path(svg_path)
	points = np.array([[p.real, p.imag] for p in (path.point(i/n_points) for i in range(n_points))])
	return points

if __name__ == '__main__':
	import matplotlib.pyplot as plt
	import sys

	def plot_points(points):
		plt.plot(center_list_of_values(points[:,0]), -1*center_list_of_values(points[:,1]), '+-')
		plt.show()

	def center_list_of_values(L):
		L = L - min(L) - max(L)/2
		return L


	filename = sys.argv[-1]
	path_list = extract_paths_from_svg_file(filename)
	print(path_list)
	points = read_svg_path_and_return_XY_tab(path_list[0], n_points=10000)

	print(points)
	plot_points(points)