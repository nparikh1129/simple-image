import itertools
from typing import Dict
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
from simple_image import SimpleImage
import simple_image_tk


class SimpleImageWindow(tk.Toplevel):
    _window_id = itertools.count(start=1)
    _windows: Dict[str, 'SimpleImageWindow'] = {}

    def __init__(self, name=None, descriptor=None):
        super().__init__(root)
        if not name:
            name = f'window{next(SimpleImageWindow._window_id)}'
        self.name = name
        self.descriptor = descriptor
        self.title(name)
        self._callbacks = {}
        self.canvas = tk.Canvas(self)
        self.image = None
        self.imagetk = None
        self.protocol("WM_DELETE_WINDOW", lambda arg=self: SimpleImageWindow._window_close(self))
        SimpleImageWindow._windows[name] = self

    @classmethod
    def update_or_create(cls, name, descriptor=None):
        if name is not None:
            window: SimpleImageWindow = SimpleImageWindow._windows.get(name)
            if window:
                window.descriptor = descriptor
                return window
        return cls(name, descriptor)

    @classmethod
    def _window_close(cls, window):
        window.destroy()
        cls._windows.pop(window.name)
        if len(cls._windows) == 0 and root.state() == 'withdrawn':
            root.destroy()

    def set_image(self, image):
        self.image = image.copy()
        self.canvas.config(width=image.width, height=image.height)
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(self.image.image_data))
        self.canvas.create_image(0, 0, anchor="nw", image=self.imagetk)
        self.canvas.pack()

    def move(self, x, y):
        self.geometry(f'+{x}+{y}')
        return self





def main():
    # root = show_tk_root()

    image1 = SimpleImage('data/futuristic_city.png')
    # image1.show('test1')
    window1 = SimpleImageWindow('test1')
    window1.set_image(image1)
    window1.move(100, 100)

    image2 = SimpleImage('data/cyberpunk.png')
    window2 = SimpleImageWindow('test2')
    window2.set_image(image2)

    SimpleImage.run()



if __name__ == '__main__':
    main()



    # def gradient(r, g, b, radius):
#     r_min, r_max = r-radius, r+radius
#     g_min, g_max = g-radius, g+radius
#     b_min, b_max = b-radius, b+radius
#
#     r_range = r_max - r_min
#     g_range = g_max - g_min
#
#     diameter = radius*2
#     b = 150
#
#     img = np.zeros((diameter, diameter, 3), dtype=np.uint8)
#     for i in range(diameter):
#         for j in range(diameter):
#
#             v1 = i/float(diameter)
#             r1 = r_range * v1
#             r = round(r1 + r_min)
#
#             v2 = j/float(diameter)
#             g2 = g_range * v2
#             g = round(g2 + g_min)
#
#             p = img[i][j]
#             if b < 0 or g < 0 or r < 0 or b > 255 or g > 255 or r > 255:
#                 p[0], p[1], p[2] = 0, 0, 0
#             else:
#                 p[0], p[1], p[2] = b, g, r
#     # for i, r in enumerate(range(r_min, r_max)):
#     #     for j, g in enumerate(range(g_min, g_max)):
#     #         for k, b in enumerate(range(b_min, b_max)):
#     #             p = img[i][j]
#     #             p[0], p[1], p[2] = b, g, r
#
#     # cv2.imshow('image', img)
#     # cv2.setWindowProperty('image', cv2.WND_PROP_TOPMOST, 1)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#     return img


# class TestApp(object):
#
#     def __init__(self):
#
#
#
#         self.root = simple_image_tk.init_tk("Tk Test")
#
#         # image1 = Image.open("data/cyberpunk.png")
#         # image1 = image1.resize((200, 200))
#         self.test1 = ImageTk.PhotoImage(file="data/cyberpunk.png")
#
#         # image2 = Image.open('data/futuristic_city.png')
#
#
#         self.canvas = tk.Canvas(self.root, width=500, height=500, bg='#777777')
#         image_container = self.canvas.create_image(0, 0, anchor="nw", image=self.test1)
#         # self.canvas.itemconfig(image_container, image=self.test1)
#         self.canvas.pack()
#
#         def update_image(r, g):
#             b = 100
#             radius = 150
#             self.img = gradient(r, g, b, radius)
#             self.test2 = ImageTk.PhotoImage(Image.fromarray(self.img))
#             self.image_container = self.canvas.create_image(0, 0, anchor="nw", image=self.test2)
#             # self.canvas.itemconfig(self.image_container, image=self.test2)
#
#         self.r = 0
#         def update(r):
#             r_new = int(float(r))
#             if r_new == self.r:
#                 return
#             self.r = r_new
#             update_image(self.r, self.r)
#
#         self.scale = ttk.Scale(self.root, from_=70, to=185, length=1000, command=update)
#         self.scale.pack()
#         # button = ttk.Button(self.root, text="Update", command=lambda: update())
#         # button.pack()
#
#
#
#
#     def run(self):
#         try:
#             self.root.mainloop()
#         finally:
#             SimpleImage.close_windows()