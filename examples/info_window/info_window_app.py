import tkinter as tk
from tkinter import ttk
from simple_image import SimpleImage, SimpleImageWindow


class LabeledValue(ttk.Frame):

    def __init__(self, parent, textvariable, width=4, label_text='', label_color=None):
        super().__init__(parent)
        self.textvariable = textvariable
        self.label = ttk.Label(self, text=label_text+':', font=("-size", 13), foreground=label_color)
        self.value = ttk.Label(self, textvariable=textvariable, font=("-size", 13), width=width)
        self.label.grid(row=0, column=0)
        self.value.grid(row=0, column=1)


class ImageInfoPanel(object):

    def __init__(self, image):
        self.img = image

        self.root = tk.Tk()
        self.root.title("Image Info")
        self.root.tk.call("source", "resources/azure-ttk-theme/azure.tcl")
        self.root.tk.call("set_theme", "dark")

        self.w_var = tk.StringVar()
        self.w_var.set('----')
        self.w_val = LabeledValue(self.root, self.w_var, label_text='W')
        self.w_val.grid(row=0, column=0)

        self.h_var = tk.StringVar()
        self.h_var.set('----')
        self.h_val = LabeledValue(self.root, self.h_var, label_text='H')
        self.h_val.grid(row=0, column=1)

        self.x_var = tk.StringVar()
        self.x_var.set('----')
        self.x_val = LabeledValue(self.root, self.x_var, label_text='X')
        self.x_val.grid(row=1, column=0)

        self.y_var = tk.StringVar()
        self.y_var.set('----')
        self.y_val = LabeledValue(self.root, self.y_var, label_text='Y')
        self.y_val.grid(row=1, column=1)

        self.r_var = tk.StringVar()
        self.r_var.set('---')
        self.r_val = LabeledValue(self.root, self.r_var, label_text='R', label_color='#F04506', width=3)
        self.r_val.grid(row=1, column=2)

        self.g_var = tk.StringVar()
        self.g_var.set('---')
        self.g_val = LabeledValue(self.root, self.g_var, label_text='G', label_color='#7BE300', width=3)
        self.g_val.grid(row=1, column=3)

        self.b_var = tk.StringVar()
        self.b_var.set('---')
        self.b_val = LabeledValue(self.root, self.b_var, label_text='B', label_color='#0594F0', width=3)
        self.b_val.grid(row=1, column=4)

        self.window_name = 'image'
        self.window = SimpleImageWindow(name=self.window_name)
        self.window.register_callback('EVENT_MOUSEMOVE', self.update_info)
        self.img.show(self.window_name)

    def update_info(self, window_name, image_data, x, y, params):
        b, g, r = image_data[y][x]
        self.w_var.set(image_data.shape[1])
        self.h_var.set(image_data.shape[0])
        self.x_var.set(x)
        self.y_var.set(y)
        self.r_var.set(r)
        self.g_var.set(g)
        self.b_var.set(b)

    def run(self):
        try:
            self.root.mainloop()
        finally:
            SimpleImage.close_windows()


def main():
    img = SimpleImage('data/cyberpunk.png')
    app = ImageInfoPanel(img)
    app.run()


if __name__ == '__main__':
    main()
