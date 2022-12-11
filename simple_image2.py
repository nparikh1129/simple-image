import itertools
from typing import Dict
import numpy as np
import cv2 as cv


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


class SimpleImageWindow(object):
    _window_id = itertools.count(start=1)
    _windows: Dict[str, 'SimpleImageWindow'] = {}

    def __init__(self, name=None, topmost=False, descriptor=None):
        if not name:
            name = f'window{next(SimpleImageWindow._window_id)}'
        self.name = name
        cv.namedWindow(name)
        if topmost:
            cv.setWindowProperty(name, cv.WND_PROP_TOPMOST, 1)
        cv.setWindowTitle(name, name)
        self.descriptor = descriptor
        self._callbacks = {}
        SimpleImageWindow._windows[name] = self

    @classmethod
    def update_or_create(cls, name, topmost=False, descriptor=None):
        if name is not None:
            window: SimpleImageWindow = SimpleImageWindow._windows.get(name)
            if window:
                if topmost:
                    cv.setWindowProperty(name, cv.WND_PROP_TOPMOST, 1)
                window.descriptor = descriptor
                return window
        return cls(name, topmost, descriptor)

    def set_image_data(self, image_data):
        # f'{name} {image_data.shape[1]}x{image_data.shape[0]}'
        param = {'window_name': self.name, 'image': image_data.copy()}
        cv.setMouseCallback(self.name, self._show_pixel_info, param)
        pass

    @staticmethod
    def _show_pixel_info(event, x, y, flags, param):
        window_name = param['window_name']
        image_data = param['image']
        b, g, r = image_data[y][x]
        window = SimpleImageWindow._windows.get(window_name)
        if event == cv.EVENT_MOUSEMOVE:
            window.invoke_callback('EVENT_MOUSEMOVE', window_name, image_data, x, y)
        elif event == cv.EVENT_LBUTTONDOWN:
            window.invoke_callback('EVENT_LBUTTONDOWN', window_name, image_data, x, y)
            pos = f"{x}, {y}"
            color = f"{r}, {g}, {b}"
            pixel_info = f"{window_name}  pos:({pos})  color:({color})"
            print(pixel_info)

    @staticmethod
    def _image_info_callback(window_name, image_data, x, y, params):
        text_color = params['text_color']
        b, g, r = image_data[y][x]
        img = image_data.copy()
        # pixel info text
        text = f"X:{x:<3}  Y:{y:<3}  R:{r:<3}  G:{g:<3}  B:{b:<3}"
        org = (5, 20)
        font = cv.FONT_HERSHEY_PLAIN
        font_scale = 1
        color = text_color
        thickness = 1
        cv.putText(img, text, org, font, font_scale, color, thickness, cv.LINE_AA)
        # pixel color box
        start_point = (307, 8)
        end_point = (317, 18)
        # outline of box
        color = text_color
        thickness = 3
        cv.rectangle(img, start_point, end_point, color, thickness)
        # color box
        pixel_color = (int(b), int(g), int(r))
        thickness = -1
        cv.rectangle(img, start_point, end_point, pixel_color, thickness)
        cv.imshow(window_name, img)

    def show_image_info(self, text_color=SimpleColor(255, 255, 255)):
        params = {'text_color': text_color.as_tuple_bgr()}
        self.register_callback('EVENT_MOUSEMOVE', self._image_info_callback, params)

    def move(self, x, y):
        cv.moveWindow(self.name, x, y)
        return self

    def register_callback(self, name, func, params=None):
        self._callbacks[name] = (func, params)

    def invoke_callback(self, name, *args):
        callback = self._callbacks.get(name)
        if callback:
            func, params = callback
            func(*args, params)


class SimpleImage(object):
    def __init__(self, filename=None):
        if filename:
            img = cv.imread(filename)
            self._img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        else:
            self._img = np.zeros((300, 400, 3), dtype=np.uint8)

    @classmethod
    def blank(cls, width=480, height=360, color=None):
        img_blank = cls()
        img_blank._img = np.zeros((height, width, 3), dtype=np.uint8)
        if color:
            img_blank._img[:] = (color.b, color.g, color.r)
        return img_blank

    @classmethod
    def from_image_data(cls, image_data: np.ndarray):
        img = cls()
        img._img = image_data
        return img

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
            if width and not height:
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
                                      value=(color.b, color.g, color.r))
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

    def show(self, window_name=None, topmost=False, descriptor=None):
        window = SimpleImageWindow.update_or_create(window_name, topmost, descriptor)
        window.set_image_data(self._img)
        cv.imshow(window.name, self._img)
        cv.waitKey(1)
        return window

    @classmethod
    def close_windows(cls):
        cv.destroyAllWindows()

    @classmethod
    def wait_key_and_close_windows(cls, delay=0):
        cv.waitKey(delay*1000)
        cv.destroyAllWindows()

    class _Pixel(object):

        def __init__(self, image, x, y):
            self._image = image
            self.x = x
            self.y = y
            self._value = image[y][x]

        @property
        def r(self):
            return int(self._value[2])

        @r.setter
        def r(self, val):
            self._value[2] = val

        @property
        def g(self):
            return int(self._value[1])

        @g.setter
        def g(self, val):
            self._value[1] = val

        @property
        def b(self):
            return int(self._value[0])

        @b.setter
        def b(self, val):
            self._value[0] = val

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
    img1 = SimpleImage('data/girl_shadows_gs.png')
    win1 = SimpleImageWindow()
    win1.show_image_info()

    img1.show(window_name=win1.name, topmost=True)
    SimpleImage.wait_key_and_close_windows(delay=120)


if __name__ == '__main__':
    main()
