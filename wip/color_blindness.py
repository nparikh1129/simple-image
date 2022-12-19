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
import threading



# class class ColorBlindnessApp(ttk.Frame):





class ColorBlindness(ttk.Frame):
    image_cache = {}

    def __init__(self, parent, img):
        super().__init__(parent)
        self.img = img
        self.image_data = img.image_data
        self.image_data_norm = img.image_data_convert(normalize=True)

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=img.width-1, height=img.height-1)
        self.image_data = self.image_data
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(self.image_data))
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.imagetk)

        self.canvas_cb = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=img.width-1, height=img.height-1)
        self.image_data_cb = self.image_data
        self.imagetk_cb = ImageTk.PhotoImage(Image.fromarray(self.image_data_cb))
        self.image_cb = self.canvas_cb.create_image(0, 0, anchor='nw', image=self.imagetk_cb)

        self.slider = simple_image_tk.SliderWithLabelAndEntry(self, label='Severity', from_=0, to=100, value=0, length=400, command=self.update)

        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, length=400)

        self.canvas.grid(row=0, column=0)
        self.canvas_cb.grid(row=0, column=1, padx=(20, 0))
        self.slider.grid(row=1, column=0)
        self.progress_bar.grid(row=2, column=0)

        thread = threading.Thread(target=self.populate_cache)
        thread.start()

    def populate_cache(self):
        for i in range(0, 101):
            if not ColorBlindness.image_cache.get(i):
                self.generate_cb_image(i)
            self.progress_var.set(i)
        print('done')

    def generate_cb_image(self, severity):
        cvd_space = {"name": "sRGB1+CVD",
                     "cvd_type": "deuteranomaly",
                     "severity": severity}
        img_cb = cspace_convert(self.image_data_norm, cvd_space, "sRGB1")
        img_cb = np.clip(img_cb, 0, 1)
        image_data_cb = (img_cb*255).astype(dtype=np.uint8)
        image = Image.fromarray(image_data_cb)
        imagetk_cb = ImageTk.PhotoImage(image)
        ColorBlindness.image_cache[severity] = imagetk_cb
        return imagetk_cb

    def update(self, severity=50):
        severity = int(severity)
        self.imagetk_cb = ColorBlindness.image_cache.get(severity)
        if not self.imagetk_cb:
            self.imagetk_cb = self.generate_cb_image(severity)
        self.canvas_cb.itemconfig(self.image_cb, image=self.imagetk_cb)





def main():
    # img = SimpleImage("data/color_blind_test.png")
    # img = SimpleImage("data/man_red_shirt_gs.png")
    # img = SimpleImage("data/color_spectrum.png")
    # img = SimpleImage("data/french_riviera.png")
    # img = SimpleImage("data/girl_black_dress_bs.png").resize_scale(0.75)
    img = SimpleImage("data/futuristic_city.png").resize_scale(0.75)
    # img = SimpleImage("data/t-rex.png")

    root = simple_image_tk.show_tk_root()
    cb = ColorBlindness(root, img)

    # img2 = SimpleImage("data/ball_pit.png").resize_scale(0.5)
    # frame = simple_image_tk.SimpleImageTk()

    cb.grid(row=0, column=0)
    # frame.grid(row=1, column=0)

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
