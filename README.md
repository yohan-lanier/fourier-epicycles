# Fourier Epicyles

A set of python methods allowing to create epicycles drawing animations using an svg file as an input
---------------------------------------------------------------------------------------------------

![sword-40](https://user-images.githubusercontent.com/72730254/179226941-c42e0747-91d7-4ed1-8c77-1b3d39f7354c.gif)

# Requirements

Code is based on python3. All required packages can be found in the requirements.txt file.
Note that this code was created on a windows system

# How to use the code

The code can be launched from a terminal by calling the script main.py and specifying the required/desired arguments. Below is the help section of the argument parser :

```
usage: main.py [-h] [-order N] [-n_points N_POINTS] [-se Start empty] [-oo Opacity on] [-head_color HEAD_COLOR] [-tail_color TAIL_COLOR]
               [-save_path SAVE_PATH]
               file

positional arguments:
  file                  String containing the path to the svg file

options:
  -h, --help            show this help message and exit
  -order N              Order of the Fourier sum, a value of N will result in 2*N+1 terms in the sum
  -n_points N_POINTS    Number of points used to discretize the svg path
  -se Start empty       A boolean used to determine if the animation starts with an empty drawing or not
  -oo Opacity on        A boolean used to determine if an opacity effect is used in the animation
  -head_color HEAD_COLOR
                        string representing the color of the head of the animation. A color gradient will be created between head and      
                        tail. Possible options are r, b, g, b, c, y, p, o, w. Default is w
  -tail_color TAIL_COLOR
                        string representing the color of the tail of the animation. A color gradient will be created between head and      
                        tail. Possible options are r, b, g, b, c, y, p, o, w. Default is w
  -save_path SAVE_PATH  if used, the animation will be saved to the location indicated by this path under the name at the end of it. The   
                        path needs to end with video-name.mp4, It should look something like c://Users/user-name/Desktop/video.mp4. Gif    
                        format is also valid
```
**@Warning : To use the save_path option, one needs to indicate the path to the matplotlib writer in the file main.py**

**@Warning 2 : If one sets -se argument to False, -oo has to be True, no exception has yet been coded to catch this**

The input svg file has to contain at list one path otherwise no animation can be rendered

# Brief and uncomplete maths explanation :

This code takes an svg path as an input. We can define a function $g : [0,1] \rightarrow \mathbb{C}$. $\forall t \in [0,1], g(t)$ represents a point of this continuous path in the complex plane. That is if $X : t \rightarrow X(t)$ is the function that represents the X coordinates of the path and $Y : t \rightarrow Y(t)$ reprensents the Y coordinates, we have $\forall t \in [0,1],  g(t) = X(t) + iY(t)$. Here, t is a fictive variable used to go through the path, in some way it can represent time. Going further we can extend g as a periodic function on $\mathbb{R}$ of period $T=1$. 

Using a Fourier Serie, we can then write : $g(t) = \Sigma_{n=-\infty}^{\infty} c_n\times e^{2i\pi nt/T}$ where $T=1$. Now the $c_n$ coefficients can be directly computed from g itself. A hint to find the formulas is to see that :

$\int_{0}^{T} g(t)dt = \int_{0}^{T}\Sigma_{n=-\infty}^{\infty} c_n\times e^{2i\pi nt/T}dt = \Sigma_{n=-\infty}^{\infty} c_n \int_{0}^{T}\times e^{2i\pi nt/T}dt = T c_0$

This is because $\forall \  n \neq 0, \ \int_{0}^{T}\times e^{2i\pi nt/T}dt = 0$ and $\int_{0}^{T}\times e^{2i\pi 0 t/T}dt =T $. **Note that there are plenty of math justifications left behind on the equation above, the most obvious one being one has to check that it is possible to swap the serie and the integral.** But for now let's just assume that everything works well. It has been found that $c_0 = \frac{1}{T}\int_{0}^{T} g(t)dt$. 

To find the other formulas, the idea is to find a way to isolate the value of each $c_n$ just as it was done above for $c_0$. It is a pretty common technique in maths when one wants to find the value of the coefficients representing the decomposition of an element of some space in a given basis of the space (which by the way is exactly what we are doing here).

On might have seen that by adding a specific exponential term to the integral of $g$ we can get what we want. Hence the seeked formula is : 

$\forall n \in \mathbb{N}, \ c_n = \frac{1}{T}\int_{0}^{T} g(t) \times e^{- 2i\pi nt/T}dt$

So now we now all the terms of the expression $g(t) = \Sigma_{n=-\infty}^{\infty} c_n\times e^{2i\pi nt/T}$ where $T=1$, but what is the link between this and the animation produced by the code ?

Well, if we evaluate $g$ at a time t=0, we will see that $g(0) = \Sigma_{n=-\infty}^{\infty} c_n$. That is, we are adding up vectors of the complex plane to get the value $g(0)$. Moreover, $e^{2i\pi nt/T}$, in the expression of $g$, simply means that the vector $c_n$ rotates in time at frequence $nt/T$ around a circle of radius $|c_n|$. **So if we add all the $c_n$ tails to heads and rotate each of them at the proper frequency, we are drawing the path described by the function $g$.**

In practice, it is not possible to compute an infinite number of terms. That's why we are using a Fourier sum, with a certain order $N$, to approximate the function g. Basically this codes computes an approximation of $g$ defined as : 
$g_N(t) = \Sigma_{n=-N}^{N} c_n\times e^{2i\pi nt/T}$ where $T=1$

Then it adds up all the $c_n$ and makes them rotate properly to create the animation.


# Relevant sources on the math behind this type of animations :

   + [An approach based on Algebra by Alex Miller](https://alex.miller.im/posts/fourier-series-spinning-circles-visualization/)
   + [Hands on introduction by 3blue1brown](https://www.youtube.com/watch?v=r6sGWTCMz2k&list=RDCMUCYO_jab_esuFRV4b17AJtAw&index=3)
   + [Interactive introduction to Fourier transform](https://www.jezzamon.com/fourier/index.html)
   + [Wikipedia on Fourier Series for maths details](https://en.wikipedia.org/wiki/Fourier_series)
