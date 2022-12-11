import colorsys
import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.geometry("+0+0")
root.tk.call("source", "resources/azure-ttk-theme/azure.tcl")
root.tk.call("set_theme", "dark")
root.withdraw()


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
        self.scale = ttk.Scale(self, from_=from_, to=to, length=self.length, variable=self._var)
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

    def _set_color(self, *args):
        h, s, b = self.slider_h.get(), self.slider_s.get(), self.slider_b.get()
        color_str = self._hsv_to_rgb_hex(h, s, b)
        self.color.create_rectangle(0, 0, 105, 105, fill=color_str)
        if self.command:
            self.command((h, s, b))


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

        self.command = None
        self._set_color()
        self.command = command

    def _set_color(self, *args):
        r, g, b = self.slider_r.get(), self.slider_g.get(), self.slider_b.get()
        color_str = f"#{r:02x}{g:02x}{b:02x}"
        self.color.create_rectangle(0, 0, 105, 105, fill=color_str)
        if self.command:
            self.command((r, g, b))


class LabeledValue(ttk.Frame):

    def __init__(self, parent, textvariable, width=4, label_text='', label_color=None):
        super().__init__(parent)
        self.textvariable = textvariable
        self.label = ttk.Label(self, text=label_text+':', font=("-size", 13), foreground=label_color)
        self.value = ttk.Label(self, textvariable=textvariable, font=("-size", 13), width=width)
        self.label.grid(row=0, column=0)
        self.value.grid(row=0, column=1)


class ImageInfoPanel(tk.Toplevel):

    def __init__(self, parent, image_window, callback=None):
        super().__init__(parent)
        self.title('Image Info')

        self.w_var = tk.StringVar()
        self.w_var.set('----')
        self.w_val = LabeledValue(self, self.w_var, label_text='W')
        self.w_val.grid(row=0, column=0)

        self.h_var = tk.StringVar()
        self.h_var.set('----')
        self.h_val = LabeledValue(self, self.h_var, label_text='H')
        self.h_val.grid(row=0, column=1)

        self.x_var = tk.StringVar()
        self.x_var.set('----')
        self.x_val = LabeledValue(self, self.x_var, label_text='X')
        self.x_val.grid(row=1, column=0)

        self.y_var = tk.StringVar()
        self.y_var.set('----')
        self.y_val = LabeledValue(self, self.y_var, label_text='Y')
        self.y_val.grid(row=1, column=1)

        self.r_var = tk.StringVar()
        self.r_var.set('---')
        self.r_val = LabeledValue(self, self.r_var, label_text='R', label_color='#F04506', width=3)
        self.r_val.grid(row=1, column=2)

        self.g_var = tk.StringVar()
        self.g_var.set('---')
        self.g_val = LabeledValue(self, self.g_var, label_text='G', label_color='#7BE300', width=3)
        self.g_val.grid(row=1, column=3)

        self.b_var = tk.StringVar()
        self.b_var.set('---')
        self.b_val = LabeledValue(self, self.b_var, label_text='B', label_color='#0594F0', width=3)
        self.b_val.grid(row=1, column=4)

        self.image_window = image_window
        self.image_window.register_callback('EVENT_MOUSEMOVE', self.update_info)
        self.protocol("WM_DELETE_WINDOW", callback)

    def update_info(self, window_name, image_data, x, y, params):
        b, g, r = image_data[y][x]
        self.w_var.set(image_data.shape[1])
        self.h_var.set(image_data.shape[0])
        self.x_var.set(x)
        self.y_var.set(y)
        self.r_var.set(r)
        self.g_var.set(g)
        self.b_var.set(b)


def show_tk_root(title=None):
    if title:
        root.title(title)
    root.deiconify()
    return root


def main():
    # color_sliders_hsb = ColorSlidersHSB(root, h=100, s=200, b=220)
    # color_sliders_rgb = ColorSlidersRGB(root, r=100, g=200, b=220)
    # color_sliders_hsb.grid(row=0, column=0)
    # color_sliders_rgb.grid(row=1, column=0, padx=(28, 0), pady=(10, 0))
    from simple_image import SimpleImage
    img = SimpleImage('data/girl_black_dress_bs.png')
    window = img.show('image')
    ImageInfoPanel(root, window, lambda: root.destroy())
    root.mainloop()
    SimpleImage.close_windows()


if __name__ == "__main__":
    main()
