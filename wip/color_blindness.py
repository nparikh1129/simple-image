from colorspacious import cspace_convert
import numpy as np
from simple_image import SimpleImage
import simple_image_tk
from simple_image_tk import SimpleImageTk, SliderWithLabelAndEntry, ButtonBar
import tkinter as tk
from tkinter import ttk
import threading

# TODO: Load images into ImagePane, don't swap out the entire frame, refactor individual image code into own class
# TODO: Resize large images to reasonable dims for severity range
# TODO: Synchronize UI and Image panes with StringVar/IntVar for single source of truth and bidirectional updates


class ImagePane(ttk.Frame):

    def __init__(self, parent, filename):
        super().__init__(parent)
        self.image = SimpleImage(filename)
        self.data = self.image.image_data
        self.data_norm = self.image.image_data_convert(normalize=True)
        self.cvd_type = 'normal'
        self.cache = {}
        self.cache_thread = threading.Thread(target=self.populate_cache, daemon=True)
        #  Configure widgets
        self.image_window = SimpleImageTk(self)
        self.severity_frame = ttk.Frame(self)
        self.progress_bar_frame = ttk.Frame(self.severity_frame)
        self.progress_bar_label = ttk.Label(self.progress_bar_frame, text='Processing severity range...', font=("-size", 13))
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.progress_bar_frame, variable=self.progress_var, length=400)
        self.slider = SliderWithLabelAndEntry(self.severity_frame, label='Severity', from_=1, to=100, value=1,
                                              length=400, command=self.update_image)
        self.image_window.grid(row=0, column=0)
        self.progress_bar_label.grid(row=0, column=0)
        self.progress_bar.grid(row=1, column=0)

    def update_image(self, *args):
        image_data_cvd = self.data_cvd(self.cvd_type)
        self.image_window.set_image_data(image_data_cvd)

    def data_cvd(self, cvd_type='normal'):
        data_cvd = self.cache.get((cvd_type, self.severity()))
        if data_cvd is None:
            data_cvd = self._generate_data_cvd(cvd_type, self.severity())
        return data_cvd

    def _generate_data_cvd(self, cvd_type, severity):
        if cvd_type == 'normal':
            return self.data
        cvd_space = {"name": "sRGB1+CVD", "cvd_type": cvd_type, "severity": severity}
        cvd = cspace_convert(self.data_norm, cvd_space, "sRGB1")
        cvd = np.clip(cvd, 0, 1)
        data_cvd = (cvd * 255).astype(dtype=np.uint8)
        self.cache[(cvd_type, severity)] = data_cvd
        return data_cvd

    def update_cvd_type(self, cvd_type):
        self.cvd_type = cvd_type
        self.update_image()

    def generate_severity_range(self):
        if self.cache_thread.is_alive():
            return
        self.cache_thread.start()

    def populate_cache(self):
        for i in range(1, 101):
            for cvd_type in ['deuteranomaly', 'tritanomaly', 'protanomaly']:
                self._generate_data_cvd(cvd_type, i)
            self.progress_var.set(i)
        self.update_severity_frame()
        self.update_image()

    def caching_completed(self):
        return int(self.progress_var.get()) >= 100

    def severity(self):
        self.update_idletasks()
        if self.slider.winfo_ismapped():
            return self.slider.get()
        return 100

    def update_show_severity(self, show_severity):
        if not show_severity:
            self.severity_frame.grid_remove()
            self.update_image()
        else:
            self.update_severity_frame()
            self.update_image()

    def update_severity_frame(self):
        self.severity_frame.grid(row=1, column=0, pady=(30, 5))
        if self.caching_completed():
            self.progress_bar_frame.grid_remove()
            self.slider.grid(row=0, column=0)
        else:
            self.progress_bar_frame.grid(row=0, column=0)
            self.generate_severity_range()


class CVDApp(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.image_pane = None
        self.image_pane_dict = {
            'Rubik\'s cube': ImagePane(self, 'data/rubiks-cube.png'),
            'French Riviera': ImagePane(self, 'data/french_riviera.png'),
            'Futuristic city': ImagePane(self, 'data/futuristic_city.png'),
            'Blue flower': ImagePane(self, 'data/blue-flower.png'),
            'Color spectrum': ImagePane(self, 'data/color_spectrum.png'),
            'RG color blindness test': ImagePane(self, 'data/color_blind_test.png'),
        }

        self.sidebar = ttk.Frame(self)
        self.sidebar_seperator = ttk.Separator(self.sidebar, orient=tk.VERTICAL)

        self.ui_frame = ttk.Frame(self.sidebar)

        self.image_chooser_frame = ttk.Frame(self.ui_frame)
        self.image_chooser_label = ttk.Label(self.image_chooser_frame, text="Select an Image", font=("-size", 16))
        self.image_chooser = ttk.Combobox(self.image_chooser_frame, state="readonly", values=list(self.image_pane_dict.keys()))
        self.image_chooser.bind('<<ComboboxSelected>>', self.image_selected)
        self.image_chooser.current(0)
        self.image_chooser_label.grid(row=0, column=0, pady=(0, 12), sticky='w')
        self.image_chooser.grid(row=1, column=0, sticky='w')

        self.cvd_types_frame = ttk.Frame(self.ui_frame)
        self.cvd_types_label = ttk.Label(self.cvd_types_frame, text="Color Blindness Types", font=("-size", 16))
        self.button_norm = ttk.Button(self.cvd_types_frame, text='Normal', command=lambda cvd_type='normal': self.update_cvd_type(cvd_type))
        self.button_deut = ttk.Button(self.cvd_types_frame, text='Deuteranomaly', command=lambda cvd_type='deuteranomaly': self.update_cvd_type(cvd_type))
        self.button_prot = ttk.Button(self.cvd_types_frame, text='Protanomaly', command=lambda cvd_type='protanomaly': self.update_cvd_type(cvd_type))
        self.button_trit = ttk.Button(self.cvd_types_frame, text='Tritanomaly', command=lambda cvd_type='tritanomaly': self.update_cvd_type(cvd_type))
        self.cvd_types_label.grid(row=0, column=0, pady=(0, 20))
        self.button_norm.grid(row=1, column=0, pady=(0, 10))
        self.button_deut.grid(row=2, column=0, pady=(10, 10))
        self.button_prot.grid(row=3, column=0, pady=(10, 10))
        self.button_trit.grid(row=4, column=0, pady=(10, 10))

        self.severity_toggle = ttk.Checkbutton(self.ui_frame, text='Show severity range', command=self.update_show_severity)
        self.severity_toggle.state(('!alternate',))

        self.sidebar.grid(row=0, column=0, sticky='ns')
        self.sidebar_seperator.grid(row=0, column=1, rowspan=2, sticky='ns')
        self.sidebar.rowconfigure(0, weight=1, minsize=100)
        self.ui_frame.grid(row=0, column=0, sticky='n', padx=(20, 20), pady=(40, 40))
        self.image_chooser_frame.grid(row=0, column=0, pady=(0, 50))
        self.cvd_types_frame.grid(row=1, column=0, pady=(0, 50))
        self.severity_toggle.grid(row=2, column=0, sticky='nw')

        self.cvd_type = 'normal'
        self.image_selected()

    def image_selected(self, *args):
        if self.image_pane:
            self.image_pane.grid_remove()
        self.image_pane = self.image_pane_dict[self.image_chooser.get()]
        self.image_pane.grid(row=0, column=1, padx=(20, 20), pady=(7, 20), sticky='n')
        self.cvd_type = 'normal'
        self.update_cvd_type(self.cvd_type)
        self.update_show_severity()

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
        self.image_pane.update_cvd_type(cvd_type)

    def update_show_severity(self):
        self.image_pane.update_show_severity(self.severity_toggle.instate(['selected']))


def main():
    root = simple_image_tk.root_(title='Color Blindness Comparison', show=False)
    app = CVDApp(root)
    app.grid(row=0, column=0)
    root.deiconify()
    root.mainloop()


if __name__ == '__main__':
    main()

