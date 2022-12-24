import time
from colorspacious import cspace_convert
import numpy as np
from simple_image import SimpleImage
import simple_image_tk
from simple_image_tk import SimpleImageTk, SliderWithLabelAndEntry, ButtonBar
import tkinter as tk
from tkinter import ttk
import threading


class CVDApp(ttk.Frame):

    class Image(object):

        def __init__(self, filename, app):
            self.app = app
            self.image = SimpleImage(filename)
            self.data = self.image.image_data
            self.data_norm = self.image.image_data_convert(normalize=True)
            self.cache = {}
            self.cache_thread = threading.Thread(target=self.populate_cache, daemon=True)

        def _generate_data_cvd(self, cvd_type, severity):
            if cvd_type == 'normal':
                return self.data
            cvd_space = {"name": "sRGB1+CVD", "cvd_type": cvd_type, "severity": severity}
            cvd = cspace_convert(self.data_norm, cvd_space, "sRGB1")
            cvd = np.clip(cvd, 0, 1)
            data_cvd = (cvd * 255).astype(dtype=np.uint8)
            self.cache[(cvd_type, severity)] = data_cvd
            return data_cvd

        def data_cvd(self, cvd_type='normal', severity=100):
            data_cvd = self.cache.get((cvd_type, severity))
            if data_cvd is None:
                data_cvd = self._generate_data_cvd(cvd_type, severity)
            return data_cvd

        def generate_severity_range(self):
            if len(self.cache) >= 100:
                return
            print(self.cache_thread.is_alive())
            self.cache_thread.start()

        def populate_cache(self):
            for i in range(1, 101):
                for cvd_type in ['deuteranomaly', 'tritanomaly', 'protanomaly']:
                    self._generate_data_cvd(cvd_type, i)
                    # self.progress_var.set(i)
                    # time.sleep(0.0001)
                print(i)
            # callback for done

    def __init__(self, parent):
        super().__init__(parent)
        self.image = None
        self.severity = 100

        self.imagepane = ttk.Frame(self)
        self.image_window = SimpleImageTk(self.imagepane)
        self.slider = SliderWithLabelAndEntry(self.imagepane, label='Severity', from_=0, to=100, value=0, length=400,
                                              command=self.update_severity)
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.imagepane, variable=self.progress_var, length=400)

        self.sidebar = ttk.Frame(self)
        self.sidebar_seperator = ttk.Separator(self.sidebar, orient=tk.VERTICAL)

        self.image_chooser_frame = ttk.Frame(self.sidebar)
        self.image_chooser_label = ttk.Label(self.image_chooser_frame, text="Select an Image", font=("-size", 16))
        self.image_dict = {
            'Rubik\'s cube': CVDApp.Image('data/rubiks-cube.png', self),
            'French Riviera': CVDApp.Image('data/french_riviera.png', self),
            'Futuristic city': CVDApp.Image('data/futuristic_city.png', self),
            'Blue flower': CVDApp.Image('data/blue-flower.png', self),
            'RG color blindness test': CVDApp.Image('data/color_blind_test.png', self)

        }
        self.image_chooser = ttk.Combobox(self.image_chooser_frame, state="readonly", values=list(self.image_dict.keys()))
        self.image_chooser.bind('<<ComboboxSelected>>', self.image_selected)
        self.image_chooser.current(0)
        self.image_chooser_label.grid(row=0, column=0, pady=(0, 12), sticky='w')
        self.image_chooser.grid(row=1, column=0)

        self.cvd_types_frame = ttk.Frame(self.sidebar)
        self.cvd_types_label = ttk.Label(self.cvd_types_frame, text="Color Blindness Types", font=("-size", 16))
        self.button_norm = ttk.Button(self.cvd_types_frame, text='Normal', command=lambda cvd_type='normal': self.update_cvd_type(cvd_type))
        self.button_deut = ttk.Button(self.cvd_types_frame, text='Deuteranomaly', command=lambda cvd_type='deuteranomaly': self.update_cvd_type(cvd_type))
        self.button_prot = ttk.Button(self.cvd_types_frame, text='Protanomaly', command=lambda cvd_type='protanomaly': self.update_cvd_type(cvd_type))
        self.button_trit = ttk.Button(self.cvd_types_frame, text='Tritanomaly', command=lambda cvd_type='tritanomaly': self.update_cvd_type(cvd_type))
        self.cvd_types_label.grid(row=0, column=0, pady=(0, 20), padx=(25, 25))
        self.button_norm.grid(row=1, column=0, pady=(0, 10))
        self.button_deut.grid(row=2, column=0, pady=(10, 10))
        self.button_prot.grid(row=3, column=0, pady=(10, 10))
        self.button_trit.grid(row=4, column=0, pady=(10, 10))

        self.severity_toggle = ttk.Checkbutton(self.sidebar, text='Show severity range', command=self.severity_toggled)
        self.severity_toggle.state(('!alternate',))

        self.close_button = ttk.Button(self.sidebar, text='Close', command=parent.destroy)

        self.imagepane.grid(row=0, column=1, padx=(20, 20), pady=(7, 20))
        self.image_window.grid(row=0, column=0)
        self.slider.grid(row=1, column=0, pady=(20, 20))
        self.progress_bar.grid(row=2, column=0)

        self.sidebar.grid(row=0, column=0, sticky='ns')
        self.sidebar.rowconfigure(2, weight=1, minsize=300)
        self.sidebar_seperator.grid(row=0, column=1, rowspan=4, sticky='ns')
        self.image_chooser_frame.grid(row=0, column=0, pady=(30, 50))
        self.cvd_types_frame.grid(row=1, column=0, padx=(20, 20), pady=(0, 30))
        self.severity_toggle.grid(row=2, column=0, sticky='n')
        self.close_button.grid(row=3, column=0, pady=(0, 20))

        self.cvd_type = 'normal'
        self.image_selected()

    def image_selected(self, *args):
        self.image = self.image_dict[self.image_chooser.get()]
        self.cvd_type = 'normal'
        self.update_cvd_type(self.cvd_type)

    def update_cvd_type(self, cvd_type):
        if cvd_type == 'normal':
            self.button_norm.configure(style='Accent.TButton')
        else:
            self.button_norm.configure(style='TButton')
        if cvd_type == 'deuteranomaly':
            self.button_deut.configure(style='Accent.TButton')
        else:
            self.button_deut.configure(style='TButton')
        if cvd_type == 'protanomaly':
            self.button_prot.configure(style='Accent.TButton')
        else:
            self.button_prot.configure(style='TButton')
        if cvd_type == 'tritanomaly':
            self.button_trit.configure(style='Accent.TButton')
        else:
            self.button_trit.configure(style='TButton')
        self.cvd_type = cvd_type
        self.update_image()

    def update_severity(self, severity):
        self.severity = int(severity)
        self.update_image()

    def update_image(self):
        image_data_cvd = self.image.data_cvd(self.cvd_type, self.severity)
        self.image_window.set_image_data(image_data_cvd)

    def severity_toggled(self):
        if 'selected' in self.severity_toggle.state():
            self.image.generate_severity_range()
        else:
            print('unselected')

def main():
    # img = SimpleImage("data/girl_shadows_gs.png")
    # img = SimpleImage("data/color_blind_test.png")
    # img = SimpleImage("data/man_red_shirt_gs.png")
    # img = SimpleImage("data/color_spectrum.png")
    # img = SimpleImage("data/french_riviera.png")
    # img = SimpleImage("data/girl_black_dress_bs.png").resize_scale(0.75)
    # img = SimpleImage("data/futuristic_city.png").resize_scale(0.75)
    # img = SimpleImage("data/t-rex.png")

    root = simple_image_tk.show_tk_root(title='Color Blindness Comparison')
    cb = CVDApp(root)
    cb.grid(row=0, column=0)
    root.mainloop()


if __name__ == '__main__':
    main()

