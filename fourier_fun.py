import sys
import cv2
import tkinter
import cmath
import numpy as np

def find_edges(image_path):
    """
    Uses opencv to find edges in an image
    """
    image = cv2.imread(image_path)
    return cv2.Canny(image, 50, 200)

def get_distance(a,b):
    """
    Gets distance between two vectors. Unused, since all the math is done with complex numbers
    """
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5

def get_complex_distance(z1,z2) -> int:
    """
    Returns the distance between two complex numbers in the complex plane
    """
    return cmath.polar(z1 - z2)[0]

def get_closest_point(points, point) -> complex:
    """
    Finds the closest point in a list of points to a starting point.
    """
    next_point = None
    dist = float('inf')

    for i in range(len(points)):
        tmp_dist = get_complex_distance(point, points[i])
        if tmp_dist < dist:
            next_point = points[i]
            dist = tmp_dist

    return next_point

def sort_points(points):
    """
    Sort the points, so that each point is the closest point to its starting point
    """
    sorted_points = [points[0]]
    points.remove(sorted_points[-1])

    while(len(points) > 0):
        sorted_points.append(get_closest_point(points, sorted_points[-1]))
        points.remove(sorted_points[-1])

    return sorted_points

def find_constant_n(points: list[tuple[int, int]], n) -> complex:
    """
    Find the n-th fourier constant using the average of all points
    """
    dt = 1 / len(points)
    c_n = 0

    for i in range(len(points)):
        t = i * dt
        c_n += dt * points[i] * cmath.e ** (-2j * cmath.pi * n * t)

    return c_n

def get_fourier_value(constants, i, t) -> complex:
    """
    this method was intended to give the center of the i+1th circle, but it didnt work.
    """
    value: complex = 0
    for a in range(i):
        #n = a//2 if a%2 == 0 else -a//2
        n = i
        value += constants[a] * cmath.e ** (n * 2j * cmath.pi * t)
    return value

def animate_epicycles(constants, width, height, scale, speed):
    """
    Draw the epicycles with their orientation lines in an tkinter canvas, and trace the path of the final fourier transformation
    """
    window = tkinter.Tk()

    drawboard = tkinter.Canvas(window, bg="black", height=height, width=width)
    drawboard.title = "Fourier Animation"
    drawboard.pack()

    circles = [drawboard.create_oval(0,0,0,0, outline="white") for i in range(len(constants))]
    lines = [drawboard.create_line(0,0,0,0, fill="white") for i in range(len(constants))]

    t = 0 # time variable
    last_position = 0
    path = []

    while True:
        t += 1

        center = 0 #complex(width / 2, height / 2)

        for i in range(1, len(constants) + 1):
            #new_center = get_fourier_value(constants, i, (t/300)) * 0.1 + complex(width / 2, height / 2)
    
            n = i//2 if i%2 == 1 else -i//2
            new_center = center + scale * constants[n + len(constants) // 2] * cmath.e ** (n * 2j * cmath.pi * t * speed)
            
            radius = cmath.polar(new_center - center)[0]

            drawboard.coords(circles[i - 1], center.real - radius, center.imag - radius, center.real + radius, center.imag + radius)
            drawboard.coords(lines[i - 1], center.real, center.imag, new_center.real, new_center.imag)
            center = new_center
        
        if last_position != 0:
            path.append(drawboard.create_line((last_position.real, last_position.imag, center.real, center.imag), width=5, capstyle='round', fill="cyan"))

        while len(path) > 2000:
            drawboard.delete(path.pop(0))

        last_position = center

        window.update()

def generate_fourier_animation(image_path, fourier_depth):
    """
    This Function is a step by step procedure to draw the edges of an image using fourier transformation and visualize the resuling function.
    
    See: https://youtu.be/r6sGWTCMz2k
    """
    print("Finding Edges ...")
    result = find_edges(image_path)

    height, width = len(result), len(result[0])

    print("Extracting all edge points ...")
    x,y = np.ndarray.nonzero(result)
    points = [complex(y[i], x[i]) for i in range(len(x))]
 
    #cv2.imwrite(os.path.join(os.path.dirname(image_path), "result.png"), result)

    print("sorting points ...")
    sorted_points = sort_points(points)

    print("Applying Fast Fourier Transform ...")
    #constants = np.fft.fft(sorted_points, fourier_depth)
    #print(constants)

    # i could not make FFT work so i used the standard math to calculate it myself.
    # Not as efficient as fft, but fast enough for demonstration.
    constants = []
    for n in range(-fourier_depth // 2, fourier_depth // 2):
        constants.append(find_constant_n(sorted_points, n))

    print("Animating Epicycles")
    animate_epicycles(constants, width, height, 1, 0.001)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Insufficient Arguments. No Image specified and/or No amount of epicycles")
        exit(1)

    generate_fourier_animation(sys.argv[1], int(sys.argv[2]))