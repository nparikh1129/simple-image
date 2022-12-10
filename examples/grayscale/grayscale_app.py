import tkinter as tk
from tkinter import ttk
from simple_image import SimpleImage
import simple_image_tk
import grayscale


class GrayscaleApp(object):

    def __init__(self, img):
        self.img = img
        self.gs_lightness = None
        self.gs_intensity = None
        self.gs_luma = None
        self.gs_lab_l = None
        self.window_name = 'image'

        self.root = simple_image_tk.init_tk(title="Grayscale")

        self.buttons_label = ttk.Label(self.root, text="Grayscale Algorithms", font=("-size", 16))
        self.buttons_frame = ttk.Frame(self.root)
        self.separator = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.button_close = ttk.Button(self.root, text='Close', command=self.root.destroy)
        # Buttons frame buttons
        self.button_img = ttk.Button(self.buttons_frame, text='Original', command=self.original)
        self.button_img_lts = ttk.Button(self.buttons_frame, text='Lightness', command=self.lightness)
        self.button_img_int = ttk.Button(self.buttons_frame, text='Intensity', command=self.intensity)
        self.button_img_lum = ttk.Button(self.buttons_frame, text='Luma 601', command=self.luma)
        self.button_img_lab = ttk.Button(self.buttons_frame, text='CIELAB L*', command=self.lab_l)

        self.buttons_label.grid(row=0, column=0, pady=(15, 5), padx=(25, 25))
        self.buttons_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 20))
        self.separator.grid(row=2, column=0, sticky='ew', pady=(10, 0))
        self.button_close.grid(row=3, column=0, pady=(15, 15))
        # Button frame buttons
        self.button_img.grid(row=0, column=0, pady=(0, 5))
        self.button_img_lts.grid(row=1, column=0, pady=(5, 5))
        self.button_img_int.grid(row=2, column=0, pady=(5, 5))
        self.button_img_lum.grid(row=3, column=0, pady=(5, 5))
        self.button_img_lab.grid(row=4, column=0, pady=(5, 0))

        self.root.update_idletasks()
        window = self.img.show(self.window_name).move(self.root.winfo_width(), 0)
        simple_image_tk.ImageInfoPanel(self.root, window)
        self.root.lift()


    def original(self):
        self.img.show(self.window_name)

    def lightness(self):
        if not self.gs_lightness:
            self.gs_lightness = grayscale.lightness(self.img.copy())
        self.gs_lightness.show(self.window_name)

    def intensity(self):
        if not self.gs_intensity:
            self.gs_intensity = grayscale.intensity(self.img.copy())
        self.gs_intensity.show(self.window_name)

    def luma(self):
        if not self.gs_luma:
            self.gs_luma = grayscale.luma601(self.img.copy())
        self.gs_luma.show(self.window_name)

    def lab_l(self):
        if not self.gs_lab_l:
            self.gs_lab_l = grayscale.cielab_lightness(self.img.copy())
        self.gs_lab_l.show(self.window_name)

    def run(self):
        try:
            self.root.mainloop()
        finally:
            SimpleImage.close_windows()


def main():
    img = SimpleImage('data/fire_breather.png')
    app = GrayscaleApp(img)
    app.run()


if __name__ == '__main__':
    main()


