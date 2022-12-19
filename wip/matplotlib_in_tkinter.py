# import itertools
# from typing import Dict
# import colorsys
# import timeit
# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# import numpy as np
# import cv2
# from simple_image import SimpleImage
# import simple_image_tk
# from simple_image_tk import SliderWithLabelAndEntry, ColorGradientHSB


import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


import numpy as np


root = tkinter.Tk()
root.wm_title("Embedding in Tk")

# fig = Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# load some test data for demonstration and plot a wireframe
X, Y, Z = axes3d.get_test_data(0.1)
ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5)

# # rotate the axes and update
# for angle in range(0, 360):
#     ax.view_init(30, angle)
#     plt.draw()
#     plt.pause(10)




canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
canvas.get_tk_widget().grid(row=0, column=0)

# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))

    Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    key_press_handler(event, canvas)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)
button.grid(row=1, column=0)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.












# def main():
#     pass
#
# if __name__ == '__main__':
#     main()
