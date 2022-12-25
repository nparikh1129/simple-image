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
        self.root = simple_image_tk.root_(title="Hue Range")
        self._h_lower = tk.IntVar()
        self._h_upper = tk.IntVar()
        self._h_lower.trace('w', self._set_h_range)
        self._h_upper.trace('w', self._set_h_range)

        self._s_lower = tk.IntVar()
        self._s_upper = tk.IntVar()
        self._s_lower.trace('w', self._set_s_range)
        self._s_upper.trace('w', self._set_s_range)

        self._b_lower = tk.IntVar()
        self._b_upper = tk.IntVar()
        self._b_lower.trace('w', self._set_b_range)
        self._b_upper.trace('w', self._set_b_range)

        self.slider_h_lower = SliderWithLabelAndEntry(self.root, label='Lower', from_=0, to=360, variable=self._h_lower)
        self.slider_h_upper = SliderWithLabelAndEntry(self.root, label='Upper', from_=0, to=360, variable=self._h_upper)
        self.color_gradient_h = ColorGradientHSB(self.root, size=200)
        self.slider_h_lower.pack()
        self.slider_h_upper.pack()
        self.color_gradient_h.pack()

        self.slider_s_lower = SliderWithLabelAndEntry(self.root, label='Lower', from_=0, to=255, variable=self._s_lower)
        self.slider_s_upper = SliderWithLabelAndEntry(self.root, label='Upper', from_=0, to=255, variable=self._s_upper)
        self.color_gradient_s = ColorGradientHSB(self.root, size=200)
        self.slider_s_lower.pack()
        self.slider_s_upper.pack()
        self.color_gradient_s.pack()

        self.slider_b_lower = SliderWithLabelAndEntry(self.root, label='Lower', from_=0, to=255, variable=self._b_lower)
        self.slider_b_upper = SliderWithLabelAndEntry(self.root, label='Upper', from_=0, to=255, variable=self._b_upper)
        self.color_gradient_b = ColorGradientHSB(self.root, size=200)
        self.slider_b_lower.pack()
        self.slider_b_upper.pack()
        self.color_gradient_b.pack()

    def _set_h_range(self, *args):
        h_lower = self.slider_h_lower.get()/360
        h_upper = self.slider_h_upper.get()/360
        ul = (h_lower, 1, 1)
        ur = (h_upper, 1, 1)
        ll = (h_lower, 1, 1)
        lr = (h_upper, 1, 1)
        self.color_gradient_h.update_gradient(ul, ur, ll, lr)
        self._set_s_range()
        self._set_b_range()

    def _set_s_range(self, *args):
        h_lower = self.slider_h_lower.get()/360
        h_upper = self.slider_h_upper.get()/360
        s_lower = self.slider_s_lower.get()/255
        s_upper = self.slider_s_upper.get()/255
        b_lower = self.slider_b_lower.get()/255
        b_upper = self.slider_b_upper.get()/255
        ul = (h_lower, s_upper, b_upper)
        ur = (h_upper, s_upper, b_upper)
        ll = (h_lower, s_lower, b_lower)
        lr = (h_upper, s_lower, b_lower)
        self.color_gradient_s.update_gradient(ul, ur, ll, lr)

    def _set_b_range(self, *args):
        h_lower = self.slider_h_lower.get()/360
        h_upper = self.slider_h_upper.get()/360
        s_lower = self.slider_s_lower.get()/255
        s_upper = self.slider_s_upper.get()/255
        b_lower = self.slider_b_lower.get()/255
        b_upper = self.slider_b_upper.get()/255
        ul = (h_lower, s_upper, b_upper)
        ur = (h_upper, s_upper, b_upper)
        ll = (h_lower, s_lower, b_lower)
        lr = (h_upper, s_lower, b_lower)
        self.color_gradient_s.update_gradient(ul, ur, ll, lr)


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