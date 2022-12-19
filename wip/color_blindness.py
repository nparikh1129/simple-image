from colorspacious import cspace_convert
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageTk
from simple_image import SimpleImage
import simple_image_tk
from simple_image_tk import SimpleImageTk, SliderWithLabelAndEntry
import tkinter as tk
from tkinter import ttk
import threading



# class class ColorBlindnessApp(ttk.Frame):





class ColorBlindness(ttk.Frame):
    image_cache = {}

    def __init__(self, parent, img):
        super().__init__(parent)
        self.img = img
        self.image_data = img.image_data
        self.image_data_cb = img.image_data
        self.image_data_norm = img.image_data_convert(normalize=True)

        self.image = SimpleImageTk(self, image_data=self.image_data, tag='cvn')
        self.slider = SliderWithLabelAndEntry(self, label='Severity', from_=0, to=100, value=0, length=400, command=self.update)
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, length=400)
        self.compare_button = ttk.Button(self, text='Compare', command=self.compare_images)

        self.image.grid(row=0, column=0, pady=(20, 0))
        self.slider.grid(row=1, column=0)
        self.progress_bar.grid(row=2, column=0)
        self.compare_button.grid(row=3, column=0)

        # TODO: Handle thread interruption gracefully
        thread = threading.Thread(target=self.populate_cache)
        thread.start()

    def compare_images(self):
        if self.image.tag == 'cvn':
            self.image.set_image_data(self.image_data_cb, tag='cvd')
        else:
            self.image.set_image_data(self.image_data, tag='cvn')


    def populate_cache(self):
        for i in range(0, 101):
            if ColorBlindness.image_cache.get(i) is None:
                self.generate_cb_image(i)
            self.progress_var.set(i)
        self.progress_bar.destroy()
        print('done')

    def generate_cb_image(self, severity):
        cvd_space = {"name": "sRGB1+CVD",
                     # "cvd_type": "tritanomaly",
                     "cvd_type": "deuteranomaly",
                     # "cvd_type": "protanomaly",
                     "severity": severity}
        img_cb = cspace_convert(self.image_data_norm, cvd_space, "sRGB1")
        img_cb = np.clip(img_cb, 0, 1)
        image_data_cb = (img_cb*255).astype(dtype=np.uint8)
        ColorBlindness.image_cache[severity] = image_data_cb
        return image_data_cb

    def update(self, severity=50):
        severity = int(severity)
        self.image_data_cb = ColorBlindness.image_cache.get(severity)
        if self.image_data_cb is None:
            self.image_data_cb = self.generate_cb_image(severity)
        self.image.set_image_data(self.image_data_cb, tag='cvd')





def main():
    # img = SimpleImage("data/girl_shadows_gs.png")
    # img = SimpleImage("data/color_blind_test.png")
    # img = SimpleImage("data/man_red_shirt_gs.png")
    # img = SimpleImage("data/color_spectrum.png")
    # img = SimpleImage("data/french_riviera.png")
    # img = SimpleImage("data/girl_black_dress_bs.png").resize_scale(0.75)
    img = SimpleImage("data/futuristic_city.png").resize_scale(0.75)
    # img = SimpleImage("data/t-rex.png")

    root = simple_image_tk.show_tk_root(title='Color Blindness Comparison')
    cb = ColorBlindness(root, img)
    cb.grid(row=0, column=0)

    root.mainloop()

if __name__ == '__main__':
    main()

