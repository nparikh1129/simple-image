import itertools
from typing import Dict
import colorsys
import timeit
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
from simple_image import SimpleImage
import simple_image_tk
from simple_image_tk import SliderWithLabelAndEntry, ColorGradientHSB


def main():
    img = SimpleImage('data/futuristic_city.png')
    img_data = img.image_data
    window = img.put_in_window()
    time = timeit.timeit(lambda: window.set_image(img_data), number=1000)
    print(time)



if __name__ == '__main__':
    main()
