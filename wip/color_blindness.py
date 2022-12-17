from colorspacious import cspace_convert
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageTk
from simple_image import SimpleImage
import simple_image_tk
import tkinter as tk
from tkinter import ttk



class ColorBlindness(ttk.Frame):

    def __init__(self, parent, img):
        super().__init__(parent)
        self.img = img
        self.image_data = img.converted_image_data(mode='RGB')
        self.image_data_norm = img.converted_image_data(mode='RGB', normalized=True)

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=img.width-1, height=img.height-1)
        self.image_data = self.image_data
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(self.image_data))
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.imagetk)

        self.canvas_cb = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=img.width-1, height=img.height-1)
        self.image_data_cb = self.image_data
        self.imagetk_cb = ImageTk.PhotoImage(Image.fromarray(self.image_data_cb))
        self.image_cb = self.canvas_cb.create_image(0, 0, anchor='nw', image=self.imagetk_cb)

        self.slider = simple_image_tk.SliderWithLabelAndEntry(parent, label='Severity', from_=0, to=100, value=0, length=400, command=self.update)

        self.canvas.grid(row=0, column=0)
        self.canvas_cb.grid(row=0, column=1, padx=(20, 0))
        self.slider.grid(row=1, column=0)

    def update(self, severity=50):
        severity = int(severity)
        cvd_space = {"name": "sRGB1+CVD",
                     "cvd_type": "deuteranomaly",
                     "severity": severity}
        img_cb = cspace_convert(self.image_data_norm, cvd_space, "sRGB1")
        img_cb = np.clip(img_cb, 0, 1)
        self.image_data_cb = (img_cb*255).astype(dtype=np.uint8)
        self.imagetk_cb = ImageTk.PhotoImage(Image.fromarray(self.image_data_cb))
        self.canvas_cb.itemconfig(self.image_cb, image=self.imagetk_cb)





def main():
    # img = SimpleImage("data/color_blind_test.png")
    # img = SimpleImage("data/man_red_shirt_gs.png")
    # img = SimpleImage("data/color_spectrum.png")
    # img = SimpleImage("data/french_riviera.png")
    img = SimpleImage("data/girl_black_dress_bs.png")
    root = simple_image_tk.show_tk_root()
    cb = ColorBlindness(root, img)
    cb.grid(row=0, column=0)
    root.mainloop()










if __name__ == '__main__':
    main()




    #
# def color_blindness(image, severity=50):
#     cvd_space = {"name": "sRGB1+CVD",
#                  "cvd_type": "deuteranomaly",
#                  "severity": severity}
#     img_cb = cspace_convert(image, cvd_space, "sRGB1")
#     img_cb = np.clip(img_cb, 0, 1)
#     img_cb = (img_cb*255).astype(dtype=np.uint8)
#     img = Image.fromarray(img_cb)
#     img.show()
