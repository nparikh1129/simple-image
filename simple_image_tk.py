import colorsys
import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.geometry("+0+0")
root.tk.call("source", "resources/azure-ttk-theme/azure.tcl")
root.tk.call("set_theme", "dark")
root.withdraw()


class LabeledValue(ttk.Frame):

    def __init__(self, parent, textvariable, width, label_text='', label_color=None, value_color=None):
        super().__init__(parent)
        self.textvariable = textvariable
        self.label = ttk.Label(self, text=label_text+':', font=("-size", 11), foreground=label_color)
        self.value = ttk.Label(self, textvariable=textvariable, font=("-size", 11), width=width, foreground=value_color)
        self.label.grid(row=0, column=0)
        self.value.grid(row=0, column=1)


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


def show_tk_root(title=None):
    if title:
        root.title(title)
    root.deiconify()
    return root


def main():
    pass


if __name__ == "__main__":
    main()
