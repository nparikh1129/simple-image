from tkinter import ttk
from simple_image import SimpleImage, SimpleColor
from simple_image_tk import init_tk, ColorSlidersRGB, SliderWithLabelAndEntry, ImageInfoPanel
import chromakey_dist


class ChromaKeyDistanceApp(object):

    def __init__(self, img_cs, img_bg):
        self.img_cs = img_cs
        self.img_bg = img_bg
        self.img = img_cs.copy()

        self.color_bg = SimpleColor(0, 0, 0)
        self.dist_max = 0

        self.root = init_tk(title="Chroma Key - Color Distance")

        self.color_sliders = ColorSlidersRGB(self.root, command=self.set_color_bg)
        self.distance_slider = SliderWithLabelAndEntry(self.root, label='Distance', from_=0, to=442, value=0,
                                                       command=self.set_color_dist)
        self.button_frame = ttk.Frame(self.root)
        self.run_button = ttk.Button(self.button_frame, text="Run Chromakey", command=self.run_chromakey)
        self.swap_button = ttk.Button(self.button_frame, text='Compare Images', command=self.swap_images)
        self.close_button = ttk.Button(self.button_frame, text='Close', command=self.root.destroy)

        self.color_sliders.grid(row=0, column=0, padx=(18, 0))
        self.distance_slider.grid(row=1, column=0, sticky='ew', padx=(10, 0))
        self.button_frame.grid(row=2, column=0, pady=(40, 10))

        self.run_button.grid(row=0, column=0, padx=(0, 16))
        self.swap_button.grid(row=0, column=1, padx=(0, 16))
        self.close_button.grid(row=0, column=3)

        self.root.update_idletasks()
        self.window_name = 'image'
        self.window = self.img.show(self.window_name, descriptor='img')
        self.window.move(self.root.winfo_width(), 0)
        ImageInfoPanel(self.root, self.window)
        self.root.lift()

    def run(self):
        try:
            self.root.mainloop()
        finally:
            SimpleImage.close_windows()

    def set_color_bg(self, rgb):
        self.color_bg = SimpleColor.from_tuple(rgb)

    def set_color_dist(self, dist):
        self.dist_max = float(dist)

    def run_chromakey(self):
        self.img = chromakey_dist.replace_background(self.img_cs.copy(), self.img_bg, self.color_bg, self.dist_max)
        self.img.show(self.window_name, descriptor='img')

    def swap_images(self):
        if self.window.descriptor == 'img':
            self.img_cs.show(self.window_name, descriptor='img_cs')
        else:
            self.img.show(self.window_name, descriptor='img')


def main():
    img_cs = SimpleImage('data/girl_black_dress_bs.png')
    img_bg = SimpleImage('data/cyberpunk.png')
    #TODO: Resize images to match
    app = ChromaKeyDistanceApp(img_cs, img_bg)
    app.run()


if __name__ == '__main__':
    main()
