import colorsys
import numpy as np
import cv2
from PIL import Image, ImageTk
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import ttk, colorchooser

# TODO: Use round() instead of int() to maintain accuracy

root = tk.Tk()
root.geometry("+0+0")
root.tk.call("source", "resources/azure-ttk-theme/azure.tcl")
root.tk.call("set_theme", "dark")
root.withdraw()
root.withdraw()


class LabeledValue(ttk.Frame):

    def __init__(self, parent, textvariable, width, label_text='', label_color=None, value_color=None):
        super().__init__(parent)
        self.textvariable = textvariable
        self.label = ttk.Label(self, text=label_text+':', font=("-size", 10), foreground=label_color)
        self.value = ttk.Label(self, textvariable=textvariable, font=("-size", 10), width=width, foreground=value_color)
        self.label.grid(row=0, column=0)
        self.value.grid(row=0, column=1)


class ImageInfoBar(ttk.Frame):

    def __init__(self, parent, color_button=True):
        super().__init__(parent)

        self.r_var = tk.StringVar(self, '---')
        self.g_var = tk.StringVar(self, '---')
        self.b_var = tk.StringVar(self, '---')
        self.x_var = tk.StringVar(self, '----')
        self.y_var = tk.StringVar(self, '----')
        self.w_var = tk.StringVar(self, '----')
        self.h_var = tk.StringVar(self, '----')

        self.r_val = LabeledValue(self, self.r_var, label_text='R', label_color='#FF4800', value_color='#C9C9C9', width=3)
        self.g_val = LabeledValue(self, self.g_var, label_text='G', label_color='#7BE300', value_color='#C9C9C9', width=3)
        self.b_val = LabeledValue(self, self.b_var, label_text='B', label_color='#019CFF', value_color='#C9C9C9', width=3)
        self.x_val = LabeledValue(self, self.x_var, label_text='X', label_color='#C9C9C9', value_color='#C9C9C9', width=4)
        self.y_val = LabeledValue(self, self.y_var, label_text='Y', label_color='#C9C9C9', value_color='#C9C9C9', width=4)
        self.w_val = LabeledValue(self, self.w_var, label_text='W', label_color='#C9C9C9', value_color='#C9C9C9', width=4)
        self.h_val = LabeledValue(self, self.h_var, label_text='H', label_color='#C9C9C9', value_color='#C9C9C9', width=4)

        if color_button:
            self.cb_img = ImageTk.PhotoImage(Image.open('resources/colorwheel.png').resize((12, 12)))
            self.color_button = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=self.cb_img.width(),
                                          height=self.cb_img.height())
            self.color_button.create_image(0, 0, anchor='nw', image=self.cb_img)
            self.color_button.bind('<Button>', lambda event: print(colorchooser.askcolor()))

        self.r_val.grid(row=0, column=0, padx=(8, 4))
        self.g_val.grid(row=0, column=1, padx=(0, 4))
        self.b_val.grid(row=0, column=2, padx=(0, 4))
        self.x_val.grid(row=0, column=3, padx=(10, 2))
        self.y_val.grid(row=0, column=4, padx=(0, 4))
        self.w_val.grid(row=0, column=5, padx=(8, 2))
        self.h_val.grid(row=0, column=6, padx=(0, 0))

        if color_button:
            self.color_button.grid(row=0, column=7, sticky='e', padx=(0, 8))
            self.grid_columnconfigure(7, weight=1)

    def update_info(self, r='---', g='---', b='---', x='----', y='----', w='----', h='----'):
        self.r_var.set(r)
        self.g_var.set(g)
        self.b_var.set(b)
        self.x_var.set(x)
        self.y_var.set(y)
        self.w_var.set(w)
        self.h_var.set(h)

    def update_dimensions(self, w, h):
        self.w_var.set(w)
        self.h_var.set(h)


class SimpleImageTk(ttk.Frame):
    def __init__(self, parent, image_data=None, tag=None, info_bar=True, color_button=False):
        super().__init__(parent)
        self.tag = tag
        self.image_data = None
        self.imagetk = None
        self.infobar = None
        self._configure_widets(image_data, info_bar, color_button)

    def _configure_widets(self, image_data, info_bar, color_button):
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas_image = self.canvas.create_image(0, 0, anchor='nw')
        if image_data is not None:
            self.set_image_data(image_data)
        self.canvas.grid(row=1, column=0)
        if info_bar:
            self.infobar = ImageInfoBar(self, color_button)
            self.infobar.grid(row=0, column=0, sticky='ew')
            self.canvas.bind('<Motion>', SimpleImageTk._mouse_action)
            self.canvas.bind('<Button>', SimpleImageTk._mouse_action)
            self.canvas.bind('<Leave>', SimpleImageTk._leave_window)

    def set_image_data(self, image_data, tag=None):
        if tag is not None:
            self.tag = tag
        width, height = image_data.shape[1], image_data.shape[0]
        self.canvas.config(width=width-1, height=height-1)
        self.image_data = image_data
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(self.image_data))
        self.canvas.itemconfig(self.canvas_image, image=self.imagetk)
        if self.infobar:
            self.infobar.update_dimensions(width, height)

    @classmethod
    def _mouse_action(cls, event):
        window = event.widget.master
        image_data = window.image_data
        r, g, b = image_data[event.y][event.x]
        x, y = event.x, event.y
        w, h = image_data.shape[1], image_data.shape[0]
        window.infobar.update_info(r, g, b, x, y, w, h)

    @classmethod
    def _leave_window(cls, event):
        window = event.widget.master
        image_data = window.image_data
        w, h = image_data.shape[1], image_data.shape[0]
        window.infobar.update_info(w=w, h=h)


class ButtonBar(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.buttons = []

    def layout_buttons(self):
        for child in self.winfo_children():
            if isinstance(child, ttk.Button):
                self.buttons.append(child)
        self.separator.grid(row=0, column=0, columnspan=len(self.buttons)+2, sticky='ew', pady=(10, 0))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(len(self.buttons)+1, weight=1)
        for i, button in enumerate(self.buttons):
            padx = (0, 16)
            if i == len(self.buttons)-1:
                padx=(0, 0)
            button.grid(row=1, column=i+1, padx=padx, pady=(15, 15))


class SliderWithLabelAndEntry(ttk.Frame):

    def __init__(self, parent, label='', from_=0, to=100, value=0, length=200, variable=None, command=None):
        super().__init__(parent)
        self.from_ = from_
        self.to = to
        self.length = length
        self.variable = variable

        self._var = tk.StringVar()
        self._var.set(str(value))
        self._var.trace_id = self._var.trace('w', self._callback)
        self.command = command

        self.label = ttk.Label(self, text=label+':', font=("-size", 13))
        self.scale = ttk.Scale(self, from_=from_, to=to, length=self.length, variable=self._var, style='Tick.TScale')
        self.entry = ttk.Entry(self, textvariable=self._var, width=3, justify=tk.RIGHT, font=("-size", 10))

        self.label.grid(row=0, column=0, sticky='e')
        self.scale.grid(row=0, column=1, sticky='ew', padx=(4, 8))
        self.entry.grid(row=0, column=2, sticky='w')

    def _callback(self, *args):
        try:
            self._var.trace_vdelete("w", self._var.trace_id)
            # Convert slider's float string value to an int string
            float_str = self._var.get()
            if not float_str:
                return
            val = min(int(float(float_str)), int(self.to))
            self._var.set(str(val))
        finally:
            self._var.trace_id = self._var.trace('w', self._callback)
        if self.variable:
            self.variable.set(self._var.get())
        if self.command:
            self.command(self._var.get())

    def get(self):
        return int(self._var.get())

    def set(self, value):
        return self._var.set(value)


class ColorBoxRGB(ttk.Frame):

    def __init__(self, parent, size=128):
        super().__init__(parent)
        self.size = size
        self.canvas = tk.Canvas(self, height=size-1, width=size-1, bg='#777777', bd=2, highlightthickness=0)
        self.color_box = self.canvas.create_rectangle(0, 0, self.size, self.size, fill='#000000')
        self.canvas.pack()

    def set_color(self, r, g, b):
        color = f"#{r:02x}{g:02x}{b:02x}"
        self.canvas.itemconfig(self.color_box, fill=color)


class ColorGradientBoxRGB(ttk.Frame):

    def __init__(self, parent, size=128):
        super().__init__(parent)
        self.size = size
        self.canvas = tk.Canvas(self, height=size-1, width=size-1, bg='#777777', bd=2, highlightthickness=0)
        self.canvas.pack()
        self.image_data = np.zeros((size, size, 3), dtype=np.uint8)
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(self.image_data))
        self.gradient_box = self.canvas.create_image(0, 0, anchor='nw', image=self.imagetk)

    @staticmethod
    def gradient_rgb(ul, ur, ll, lr, size):
        row_first = np.linspace(ul, ur, num=size)
        row_last = np.linspace(ll, lr, num=size)
        gradient = np.linspace(row_first, row_last, num=size)
        image_data = gradient.astype('uint8')
        return image_data

    def set_gradient(self, ul, ur, ll, lr):
        self.image_data = self.gradient_rgb(ul, ur, ll, lr, self.size)
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(self.image_data))
        self.canvas.itemconfig(self.gradient_box, image=self.imagetk)


class ColorGradientHSB(ttk.Frame):

    def __init__(self, parent, size):
        super().__init__(parent)
        self.size = size
        self.canvas = tk.Canvas(self, height=size-1, width=size-1, bg='#777777', bd=2, highlightthickness=0)
        self.canvas.pack()
        self.image_data = np.zeros((size, size, 3), dtype=np.uint8)
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(self.image_data))
        self.canvas.create_image(0, 0, anchor='nw', image=self.imagetk)

    @staticmethod
    def gradient_hsb(ul, ur, ll, lr, size):
        row_first = np.linspace(ul, ur, num=size)
        row_last = np.linspace(ll, lr, num=size)
        hsv = np.linspace(row_first, row_last, num=size)
        rgb = mcolors.hsv_to_rgb(hsv)
        image_data = (rgb*255).astype('uint8')
        return image_data

    def update_gradient(self, ul, ur, ll, lr):
        self.image_data = self.gradient_hsb(ul, ur, ll, lr, self.size)
        self.imagetk = ImageTk.PhotoImage(Image.fromarray(self.image_data))
        self.canvas.create_image(0, 0, anchor='nw', image=self.imagetk)


class ColorSlidersHSB(ttk.Frame):

    def __init__(self, parent, h=0, s=0, b=0, command=None):
        super().__init__(parent)

        self._h = tk.IntVar()
        self._s = tk.IntVar()
        self._b = tk.IntVar()
        self._h.trace('w', self._set_color)
        self._s.trace('w', self._set_color)
        self._b.trace('w', self._set_color)

        self.slider_h = SliderWithLabelAndEntry(self, label='Hue', from_=0, to=179, value=h, variable=self._h)
        self.slider_s = SliderWithLabelAndEntry(self, label='Saturation', from_=0, to=255, value=s, variable=self._s)
        self.slider_b = SliderWithLabelAndEntry(self, label='Brightness', from_=0, to=255, value=b, variable=self._b)
        self.color = tk.Canvas(self, height=100, width=100, bg='#777777', bd=2)

        self.slider_h.grid(row=0, column=0, sticky='e', padx=8, pady=(8, 2))
        self.slider_s.grid(row=1, column=0, sticky='e', padx=8, pady=2)
        self.slider_b.grid(row=2, column=0, sticky='e', padx=8, pady=(2, 8))
        self.color.grid(row=0, column=3, rowspan=3, sticky='e', padx=10, pady=8)

        self.color.bind('<Button>', self._choose_color)

        self.command = None
        self._set_color()
        self.command = command

    @staticmethod
    def _hsv_to_rgb_hex(h, s, v):
        h, s, v = h/179, s/255, v/255
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r, g, b = (int(r*255), int(g*255), int(b*255))
        rgb_hex = f"#{r:02x}{g:02x}{b:02x}"
        return rgb_hex

    @staticmethod
    def _rgb_to_hsv(r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h, s, v = round(h*179), round(s*255), round(v)
        return h, s, v

    def _set_color(self, *args):
        h, s, b = self.slider_h.get(), self.slider_s.get(), self.slider_b.get()
        color_str = self._hsv_to_rgb_hex(h, s, b)
        self.color.create_rectangle(0, 0, 105, 105, fill=color_str)
        if self.command:
            self.command((h, s, b))

    def _choose_color(self, event):
        color = colorchooser.askcolor()
        if not color or not color[0]:
            return
        h, s, b = self._rgb_to_hsv(*color[0])
        self.slider_h.set(h)
        self.slider_s.set(s)
        self.slider_b.set(b)


class ColorSlidersRGB(ttk.Frame):

    def __init__(self, parent, r=0, g=0, b=0, command=None):
        super().__init__(parent)

        self._r = tk.IntVar()
        self._g = tk.IntVar()
        self._b = tk.IntVar()
        self._r.trace('w', self._set_color)
        self._g.trace('w', self._set_color)
        self._b.trace('w', self._set_color)

        self.slider_r = SliderWithLabelAndEntry(self, label='Red', from_=0, to=255, value=r, variable=self._r)
        self.slider_g = SliderWithLabelAndEntry(self, label='Green', from_=0, to=255, value=g, variable=self._g)
        self.slider_b = SliderWithLabelAndEntry(self, label='Blue', from_=0, to=255, value=b, variable=self._b)
        self.color = tk.Canvas(self, height=100, width=100, bg='#777777', bd=2)

        self.slider_r.grid(row=0, column=0, sticky='e', padx=8, pady=(8, 2))
        self.slider_g.grid(row=1, column=0, sticky='e', padx=8, pady=2)
        self.slider_b.grid(row=2, column=0, sticky='e', padx=8, pady=(2, 8))
        self.color.grid(row=0, column=3, rowspan=3, sticky='e', padx=10, pady=8)

        self.color.bind('<Button>', self._choose_color)

        self.command = None
        self._set_color()
        self.command = command

    def _set_color(self, *args):
        r, g, b = self.slider_r.get(), self.slider_g.get(), self.slider_b.get()
        color_str = f"#{r:02x}{g:02x}{b:02x}"
        self.color.create_rectangle(0, 0, 105, 105, fill=color_str)
        if self.command:
            self.command((r, g, b))

    def _choose_color(self, event):
        color = colorchooser.askcolor()
        if not color or not color[0]:
            return
        r, g, b = color[0]
        self.slider_r.set(round(r))
        self.slider_g.set(round(g))
        self.slider_b.set(round(b))


def show_tk_root(title=None):
    if title:
        root.title(title)
    root.deiconify()
    return root


def main():
    pass


if __name__ == "__main__":
    main()
