from tkinter import ttk
import numpy as np
import cv2 as cv

from simple_image import SimpleImage
import simple_image_tk
import chromakey


class ChromaKeyApp(object):

    def __init__(self, img_cs, img_bg):
        self.img_cs = img_cs
        self.img_bg = img_bg
        self.img_composite = img_cs.copy()
        self.img_hsb = cv.cvtColor(img_cs, cv.COLOR_BGR2HSV)
        self.hsb_l = np.array([0, 0, 0])
        self.hsb_u = np.array([0, 0, 0])
        self.window_name = 'Chroma Screen Image'

        # UI elements config
        self.root = simple_image_tk.show_tk_root('Threshold Selector')
        self.label_l = ttk.Label(self.root, text="Lower Threshold", font=("-size", 16))
        self.color_sliders_hsb_l = simple_image_tk.ColorSlidersHSB(self.root, h=self.hsb_l[0], s=self.hsb_l[1],
                                                                 b=self.hsb_l[2], command=self.update_hsb_lower)
        self.label_u = ttk.Label(self.root, text="Upper Threshold", font=("-size", 16))
        self.color_sliders_hsb_u = simple_image_tk.ColorSlidersHSB(self.root, h=self.hsb_u[0], s=self.hsb_u[1],
                                                                 b=self.hsb_u[2], command=self.update_hsb_upper)
        self.buttons_bar = simple_image_tk.ButtonsBar(self.root)
        self.swap_button = ttk.Button(self.buttons_bar, text='Compare Images', command=self.swap_images)
        self.close_button = ttk.Button(self.buttons_bar, text='Close', command=self.root.destroy)

        # UI elements layout
        self.label_l.grid(row=0, column=0, columnspan=1, pady=(10, 0), padx=(0, 90))
        self.color_sliders_hsb_l.grid(row=1, column=0)
        self.label_u.grid(row=2, column=0, columnspan=1, pady=(30, 0), padx=(0, 90))
        self.color_sliders_hsb_u.grid(row=3, column=0, pady=(10, 0))
        self.buttons_bar.grid(row=4, column=0, pady=(30, 0), sticky='ew')
        self.buttons_bar.layout_buttons()

        # Windows layout
        self.root.update_idletasks()
        self.window = SimpleImage.from_image_data(img_cs, mode='BGR').put_in_window(self.window_name, tag='chromascreen')
        self.window.move(self.root.winfo_width(), 0)
        self.root.lift()

    def update_hsb_lower(self, hsb):
        self.hsb_l[0], self.hsb_l[1], self.hsb_l[2] = hsb
        self.img_composite = chromakey.run(self.img_cs, self.img_bg, self.img_hsb, self.hsb_l, self.hsb_u)
        si_img_composite = SimpleImage.from_image_data(self.img_composite, mode='BGR')
        self.window = si_img_composite.put_in_window(self.window_name, tag='composite')

    def update_hsb_upper(self, hsb):
        self.hsb_u[0], self.hsb_u[1], self.hsb_u[2] = hsb
        self.img_composite = chromakey.run(self.img_cs, self.img_bg, self.img_hsb, self.hsb_l, self.hsb_u)
        si_img_composite = SimpleImage.from_image_data(self.img_composite, mode='BGR')
        self.window = si_img_composite.put_in_window(self.window_name, tag='composite')

    def swap_images(self):
        if self.window.tag == 'chromascreen':
            si_img_composite = SimpleImage.from_image_data(self.img_composite, mode='BGR')
            si_img_composite.put_in_window(self.window_name, tag='composite')
        else:
            si_img_cs = SimpleImage.from_image_data(self.img_cs, mode='BGR')
            si_img_cs.put_in_window(self.window_name, tag='chromascreen')


def main():
    img_cs = cv.imread('data/girl_shadows_gs.png')
    img_bg = cv.imread('data/cyberpunk.png')
    img_bg = cv.resize(img_bg, (img_cs.shape[1], img_cs.shape[0]))
    ChromaKeyApp(img_cs, img_bg)
    SimpleImage.show_windows()


if __name__ == '__main__':
    main()
