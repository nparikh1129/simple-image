import itertools
from typing import Dict
import numpy as np
import cv2 as cv
from PIL import Image
import tkinter as tk

import simple_image_tk
from simple_image_tk import root

# TODO: Any reason not to base most of this on pillow?


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
    _windows: Dict[str, 'SimpleImageWindow'] = {}
    _window_id = itertools.count(start=1)

    def __init__(self, name=None, title=None):
        super().__init__(root)
        if not name:
            name = f'window{next(SimpleImageWindow._window_id)}'
        self.title(title or name)
        self.image = simple_image_tk.SimpleImageTk(self, name)
        self.protocol("WM_DELETE_WINDOW", lambda arg=self: SimpleImageWindow._window_close(arg))
        self.image.grid(row=0, column=0)

    @classmethod
    def update_or_create(cls, name=None, title=None):
        if name is not None:
            window: SimpleImageWindow = cls._windows.get(name)
            if window:
                if title is not None:
                    window.title(title)
                return window
        window = SimpleImageWindow(name=name, title=title)
        cls._windows[window.name] = window
        return window

    def _window_close(self):
        self.destroy()
        SimpleImageWindow._windows.pop(self.image.name)
        if len(SimpleImageWindow._windows) == 0 and root.state() == 'withdrawn':
            root.destroy()

    @property
    def name(self):
        return self.image.name

    def set_image_data(self, image_data):
        self.image.set_image_data(image_data)

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

    def image_data_convert(self, mode='RGB', normalize=False):
        image_data = self._img.copy()
        if mode == 'RGB':
            if normalize:
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

    def put_in_window(self, window_name=None, title=None):
        window = SimpleImageWindow.update_or_create(window_name, title)
        window.set_image_data(self.image_data.copy())
        return window

    @classmethod
    def show_windows(cls):
        root.mainloop()

    def show(self, title=None):
        image = Image .fromarray(self.image_data)
        image.show(title=title)

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
    # window1 = image1.put_in_window(window_name='test1')
    # print(id(window1))

    image1.show('My image')

    image2 = SimpleImage('data/cyberpunk.png')
    window2 = image2.put_in_window(window_name='test2')
    print(id(window2))

    SimpleImage.show_windows()


if __name__ == '__main__':
    main()
