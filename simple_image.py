import itertools
from typing import Dict
import numpy as np
import cv2 as cv
from PIL import Image, ImageTk
import tkinter as tk
from simple_image_tk import root, ImageInfoBar

# TODO: Use pillow for imageio

class SimpleColor(object):

    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def from_tuple(cls, rgb):
        return cls(*rgb)

    def as_tuple(self):
        return self.r, self.g, self.b

    def as_tuple_bgr(self):
        return self.b, self.g, self.r


class SimpleImageWindow(tk.Toplevel):
    _window_id = itertools.count(start=1)
    _windows: Dict[str, 'SimpleImageWindow'] = {}

    def __init__(self, name=None, tag=None):
        super().__init__(root)
        if not name:
            name = f'window{next(SimpleImageWindow._window_id)}'
        self.name = name
        self.title(name)
        self.tag = tag
        self._configure_widets()
        SimpleImageWindow._windows[name] = self

    def _configure_widets(self):
        self.infobar = ImageInfoBar(self)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.infobar.grid(row=0, column=0, sticky='ew')
        self.canvas.grid(row=1, column=0)
        self.image = None
        self.imagetk = None
        self.canvas.bind('<Motion>', SimpleImageWindow._mouse_action)
        self.canvas.bind('<Button>', SimpleImageWindow._mouse_action)
        self.canvas.bind('<Leave>', SimpleImageWindow._leave_window)
        self.protocol("WM_DELETE_WINDOW", lambda arg=self: SimpleImageWindow._window_close(self))

    @classmethod
    def _update_or_create(cls, name, tag=None):
        if name is not None:
            window: SimpleImageWindow = SimpleImageWindow._windows.get(name)
            if window:
                window.tag = tag
                return window
        return cls(name, tag)

    def set_image(self, image):
        self.image = image.copy()
        self.canvas.config(width=image.width-1, height=image.height-1)
        image_data = self.image.image_data
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(image_data))
        # TODO: Update the canvas image instead of creating if the canvas image already exists
        self.canvas.create_image(0, 0, anchor='nw', image=self.imagetk)

    @classmethod
    def _window_close(cls, window):
        window.destroy()
        cls._windows.pop(window.name)
        if len(cls._windows) == 0 and root.state() == 'withdrawn':
            root.destroy()

    @classmethod
    def _mouse_action(cls, event):
        window = event.widget.master
        image_data = window.image.image_data
        r, g, b = image_data[event.y][event.x]
        x, y = event.x, event.y
        w, h = image_data.shape[1], image_data.shape[0]
        window.infobar.update_info(r, g, b, x, y, w, h)

    @classmethod
    def _leave_window(cls, event):
        window = event.widget.master
        image_data = window.image.image_data
        w, h = image_data.shape[1], image_data.shape[0]
        window.infobar.update_info(w=w, h=h)

    def move(self, x, y):
        self.geometry(f'+{x}+{y}')
        return self


class SimpleImage(object):
    def __init__(self, filename=None):
        if filename:
            self._img = cv.cvtColor(cv.imread(filename), cv.COLOR_BGR2RGB)
        else:
            self._img = np.zeros((300, 400, 3), dtype=np.uint8)

    @classmethod
    def blank(cls, width=480, height=360, color=None):
        img_blank = cls()
        img_blank._img = np.zeros((height, width, 3), dtype=np.uint8)
        if color:
            img_blank._img[:] = (color.r, color.g, color.b)
        return img_blank

    @classmethod
    def from_image_data(cls, image_data: np.ndarray, mode='RGB', normalized=False):
        image_data = image_data.copy()
        if mode == 'BGR':
            image_data = cv.cvtColor(image_data, cv.COLOR_BGR2RGB)
        if (mode == 'RGB' or mode == 'BGR') and normalized:
            image_data = (image_data*255).astype(dtype=np.uint8)
        img = cls()
        img._img = image_data
        return img

    def image_data_converted(self, mode='RGB', normalized=False):
        image_data = self._img.copy()
        if mode == 'RGB':
            if normalized:
                image_data = image_data/255
        return image_data

    @property
    def height(self):
        return self._img.shape[0]

    @property
    def width(self):
        return self._img.shape[1]

    @property
    def image_data(self) -> np.ndarray:
        return self._img

    @image_data.setter
    def image_data(self, image_data: np.ndarray):
        self._img = image_data

    def write(self, filename):
        cv.imwrite(filename, self._img)
        print('image written to ' + filename)

    def copy(self):
        img_copy = SimpleImage.blank(self.width, self.height)
        img_copy._img = self._img.copy()
        return img_copy

    def resize(self, width, height):
        self._img = cv.resize(self._img, (int(width), int(height)))
        return self

    def resize_scale(self, factor):
        return self.resize(self.width*factor, self.height*factor)

    def resize_proportional(self, width=None, height=None):
        if width or height:
            if width:
                factor = (width/self.width)
            else:
                factor = (height/self.height)
            self.resize_scale(factor)
        return self

    def resize_crop(self, width, height):
        w1, h1 = float(self.width), float(self.height)
        w2, h2 = float(width), float(height)
        ratio1 = w1 / h1
        ratio2 = w2 / h2
        if ratio1 != ratio2:
            if ratio1 < ratio2:
                crop_width = w1
                crop_height = w1 * (h2 / w2)
            else:
                crop_width = h1 * (w2 / h2)
                crop_height = h1
            self.crop_center(crop_width, crop_height)
        return self.resize(width, height)

    def add_border(self, top=0, bottom=0, left=0, right=0, color=SimpleColor(0, 0, 0)):
        self._img = cv.copyMakeBorder(self._img, top, bottom, left, right, cv.BORDER_CONSTANT, None,
                                       value=(color.r, color.g, color.b))
        return self

    def add_border_centered(self, width, height, color=SimpleColor(0, 0, 0)):
        if width >= self.width and height >= self.height:
            tb = int((height - self.height) / 2)
            lr = int((width - self.width) / 2)
            self.add_border(tb, tb, lr, lr, color)
        return self

    def crop(self, x1, y1, x2, y2):
        self._img = self._img[y1:y2, x1:x2]
        return self

    def crop_center(self, width, height):
        x1 = int((self.width - width) / 2)
        y1 = int((self.height - height) / 2)
        x2 = int(x1 + width)
        y2 = int(y1 + height)
        return self.crop(x1, y1, x2, y2)

    def paste(self, img: 'SimpleImage', x, y):
        self._img[y:y + img.height, x:x + img.width] = img._img
        return self

    def show(self, window_name=None, tag=None):
        window = SimpleImageWindow._update_or_create(window_name, tag)
        window.set_image(self)
        return window

    # TODO: Provide an method for getting the window as an embeddable Frame instead of Toplevel

    @classmethod
    def run(cls):
        root.mainloop()

    class _Pixel(object):

        def __init__(self, image, x, y):
            self._image = image
            self.x = x
            self.y = y
            self._value = image[y][x]

        @property
        def r(self):
            return int(self._value[0])

        @r.setter
        def r(self, val):
            self._value[0] = val

        @property
        def g(self):
            return int(self._value[1])

        @g.setter
        def g(self, val):
            self._value[1] = val

        @property
        def b(self):
            return int(self._value[2])

        @b.setter
        def b(self, val):
            self._value[2] = val

        def __str__(self):
            return f"x:{self.x} y:{self.y} r:{self.r} g:{self.g} b:{self.b}"

    def get_pixel(self, x, y):
        return self._Pixel(self._img, x, y)

    def __iter__(self):
        self._x = 0
        self._y = 0
        return self

    def __next__(self):
        if self._y >= self.height:
            raise StopIteration
        pixel = self._Pixel(self._img, self._x, self._y)
        if self._x < self.width - 1:
            self._x += 1
        else:
            self._x = 0
            self._y += 1
        return pixel


def main():
    image1 = SimpleImage('data/girl_black_dress_bs.png')
    window1 = image1.show('test1')

    image2 = SimpleImage('data/cyberpunk.png')
    image2.show()

    SimpleImage.run()


if __name__ == '__main__':
    main()
