import itertools
from typing import Dict
import colorsys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
from simple_image import SimpleImage
import simple_image_tk
from simple_image_tk import SliderWithLabelAndEntry, ColorGradientHSB


class HueRangeApp(object):

    def __init__(self):
        self.root = simple_image_tk.show_tk_root(title="Hue Range")
        self._h_lower = tk.IntVar()
        self._h_upper = tk.IntVar()
        self._h_lower.trace('w', self._set_color)
        self._h_upper.trace('w', self._set_color)

        self.slider_h_lower = SliderWithLabelAndEntry(self.root, label='Lower', from_=0, to=360, variable=self._h_lower)
        self.slider_h_upper = SliderWithLabelAndEntry(self.root, label='Upper', from_=0, to=360, variable=self._h_upper)
        self.color_gradient = ColorGradientHSB(self.root, size=100)

        self.slider_h_lower.pack()
        self.slider_h_upper.pack()
        self.color_gradient.pack()

    def _set_color(self, *args):
        h_lower = self.slider_h_lower.get()/360
        h_upper = self.slider_h_upper.get()/360
        ul = (h_lower, 1, 1)
        ur = (h_upper, 1, 1)
        ll = (h_lower, 1, 1)
        lr = (h_upper, 1, 1)
        self.color_gradient.update_gradient(ul, ur, ll, lr)

    def run(self):
        self.root.mainloop()


def main():
    app = HueRangeApp()
    app.run()


if __name__ == '__main__':
    main()




# def gradient_canvas(parent, image_data):
#     canvas = tk.Canvas(parent)
#     canvas.config(width=image_data.shape[1]-1, height=image_data.shape[0]-1)
#     imagetk = ImageTk.PhotoImage(Image.fromarray(image_data))
#     canvas.create_image(0, 0, anchor='nw', image=imagetk)
#     return canvas
#
#
# def gradient_hsb(ul, ur, ll, lr, size):
#     row_first = np.linspace(ul, ur, num=size, dtype=np.uint8)
#     row_last = np.linspace(ll, lr, num=size, dtype=np.uint8)
#     image_data_hsv = np.linspace(row_first, row_last, num=size, dtype=np.uint8)
#     image_data = cv2.cvtColor(image_data_hsv, cv2.COLOR_HSV2BGR)
#     return image_data
#
#
# def main():
#     ul = [0, 255, 255]
#     ur = [179, 255, 255]
#     ll = [0, 255, 255]
#     lr = [179, 255, 255]
#     image_data = gradient_hsb(ul, ur, ll, lr, 200)
#
#     root = simple_image_tk.show_tk_root()
#     image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
#     canvas = tk.Canvas(root)
#     canvas.config(width=image_data.shape[1]-1, height=image_data.shape[0]-1)
#     imagetk = ImageTk.PhotoImage(Image.fromarray(image_data))
#     canvas.create_image(0, 0, anchor='nw', image=imagetk)
#
#     canvas.pack()
#     root.mainloop()