# fourier-fun
This Python script is a small command line tool that can draw the outlines of an input image by only using animatated epicycles, generated by a fourier transform.

## Setup
run `pip install -r requirements.txt` to install all PIP Dependencies.
Additionally, you have to install Tkinter for the graphical output.

## Usage
You have to pass two arguments to the script: A valid path to an image and the amount of fourier calculation steps.
- Example: `python3 fourier_fun.py 'image.py' 250`