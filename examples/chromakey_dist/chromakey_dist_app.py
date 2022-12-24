from tkinter import ttk

import simple_image_tk
from simple_image import SimpleImage, SimpleColor
from simple_image_tk import ColorSlidersRGB, SliderWithLabelAndEntry
import chromakey_dist


class ChromaKeyDistanceApp(object):

    def __init__(self, img_cs, img_bg):
        self.img_cs = img_cs
        self.img_bg = img_bg
        self.img = img_cs.copy()

        self.color_bg = SimpleColor(0, 0, 0)
        self.dist_max = 0

        self.root = simple_image_tk.show_tk_root(title="Chroma Key - Color Distance")

        self.color_label = ttk.Label(self.root, text="Target Color", font=("-size", 16))
        self.color_sliders = ColorSlidersRGB(self.root, command=self.set_color_bg)
        self.distance_label = ttk.Label(self.root, text="Color Difference", font=("-size", 16))
        self.distance_slider = SliderWithLabelAndEntry(self.root, label='Distance', from_=0, to=442, value=0,
                                                       command=self.set_color_dist)
        self.buttons_bar = simple_image_tk.ButtonBar(self.root)
        self.run_button = ttk.Button(self.buttons_bar, text="Run Chromakey", command=self.run_chromakey)
        self.swap_button = ttk.Button(self.buttons_bar, text='Compare Images', command=self.swap_images)
        self.close_button = ttk.Button(self.buttons_bar, text='Close', command=self.root.destroy)

        self.color_label.grid(row=0, column=0, columnspan=1, pady=(20, 0), padx=(0, 90))
        self.color_sliders.grid(row=1, column=0, padx=(18, 0))
        self.distance_label.grid(row=2, column=0, columnspan=1, pady=(20, 10), padx=(0, 90))
        self.distance_slider.grid(row=3, column=0, sticky='ew', padx=(10, 0))
        self.buttons_bar.grid(row=4, column=0, pady=(35, 0), sticky='ew')
        self.buttons_bar.layout_buttons()

        self.root.update_idletasks()
        self.window_name = 'Chroma Screen Image'
        self.window = self.img.put_in_window(self.window_name, tag='img')
        self.window.move(self.root.winfo_width(), 0)
        self.root.lift()

    def run(self):
        self.root.mainloop()

    def set_color_bg(self, rgb):
        self.color_bg = SimpleColor.from_tuple(rgb)

    def set_color_dist(self, dist):
        self.dist_max = float(dist)

    def run_chromakey(self):
        self.img = chromakey_dist.replace_background(self.img_cs.copy(), self.img_bg, self.color_bg, self.dist_max)
        self.img.put_in_window(self.window_name, tag='img')

    def swap_images(self):
        if self.window.tag == 'img':
            self.img_cs.put_in_window(self.window_name, tag='img_cs')
        else:
            self.img.put_in_window(self.window_name, tag='img')

# TODO: Be able to choose cs and bg images, including blank backgrounds
def main():
    img_cs = SimpleImage('data/girl_shadows_gs.png')
    img_bg = SimpleImage('data/cyberpunk.png')
    #TODO: Resize images to match
    app = ChromaKeyDistanceApp(img_cs, img_bg)
    app.run()


if __name__ == '__main__':
    main()
