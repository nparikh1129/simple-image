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


def main():
    size = 500

    root = simple_image_tk.root_()
    color_box = simple_image_tk.ColorBoxRGB(root, size)
    color_box.set_color(0, 0, 0)


    def _move_color_zoom(event):
        x, y = event.x, event.y
        x = min(max(x, 0), size)
        y = min(max(y, 0), size)
        g = round(x * (255/500))
        r = round((size-y) * (255/500))
        slider_g.set(g)
        slider_r.set(r)


    def _change_b(event):
        b = slider_b.get()
        b += event.delta
        b = min(max(b, 0), 255)
        slider_b.set(b)


    gradient_box = simple_image_tk.ColorGradientBoxRGB(root, size)
    ul = (255, 0, 0)
    ur = (255, 255, 0)
    ll = (0, 0, 0)
    lr = (0, 255, 0)
    gradient_box.set_gradient(ul, ur, ll, lr)
    line_g = gradient_box.canvas.create_line(0, 0, 0, size, fill='white')
    line_r = gradient_box.canvas.create_line(0, size, size, size, fill='white')
    color_zoom = gradient_box.canvas.create_rectangle(0, 0, 9, 9, fill='#000000', outline='white')
    gradient_box.canvas.bind('<Button>', _move_color_zoom)
    gradient_box.canvas.bind('<B1-Motion>', _move_color_zoom)
    gradient_box.canvas.bind('<MouseWheel>', _change_b)




    def _set_color(*args):
        r, g, b = slider_r.get(), slider_g.get(), slider_b.get()
        color_box.set_color(r, g, b)
        g_ = g*(size/255)
        r_ = r*(size/255)
        gradient_box.canvas.coords(line_g, g_, 0, g_, size)
        gradient_box.canvas.coords(line_r, 0, size-r_, size, size-r_)
        gradient_box.canvas.coords(color_zoom, g_-4, size-r_+4, g_+4, size-r_-4)
        gradient_box.canvas.itemconfig(color_zoom, fill=f"#{r:02x}{g:02x}{b:02x}")
        if args[0] == 'VAR_R' or args[0] == 'VAR_G':
            return
        ul = (255, 0, b)
        ur = (255, 255, b)
        ll = (0, 0, b)
        lr = (0, 255, b)
        gradient_box.set_gradient(ul, ur, ll, lr)

    _r = tk.IntVar(name='VAR_R')
    _g = tk.IntVar(name='VAR_G')
    _b = tk.IntVar(name='VAR_B')
    _r.trace('w', _set_color)
    _g.trace('w', _set_color)
    _b.trace('w', _set_color)

    slider_r = simple_image_tk.SliderWithLabelAndEntry(root, label='Red', from_=0, to=255, value=0, length=400, variable=_r)
    slider_g = simple_image_tk.SliderWithLabelAndEntry(root, label='Green', from_=0, to=255, value=0, length=400, variable=_g)
    slider_b = simple_image_tk.SliderWithLabelAndEntry(root, label='Blue', from_=0, to=255, value=0, length=400, variable=_b)

    gradient_box.grid(row=0, column=0)
    color_box.grid(row=0, column=1, padx=(20, 0))

    slider_r.grid(row=1, column=0, columnspan=2, sticky='w', pady=(20, 0))
    slider_g.grid(row=2, column=0, columnspan=2, sticky='w', pady=(20, 0))
    slider_b.grid(row=3, column=0, columnspan=2, sticky='w', pady=(20, 0))

    root.mainloop()


if __name__ == '__main__':
    main()
