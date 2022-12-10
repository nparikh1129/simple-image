import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
from simple_image import SimpleImage
import simple_image_tk


def gradient(r, g, b, radius):
    r_min, r_max = r-radius, r+radius
    g_min, g_max = g-radius, g+radius
    b_min, b_max = b-radius, b+radius

    r_range = r_max - r_min
    g_range = g_max - g_min

    diameter = radius*2
    b = 150

    img = np.zeros((diameter, diameter, 3), dtype=np.uint8)
    for i in range(diameter):
        for j in range(diameter):

            v1 = i/float(diameter)
            r1 = r_range * v1
            r = round(r1 + r_min)

            v2 = j/float(diameter)
            g2 = g_range * v2
            g = round(g2 + g_min)

            p = img[i][j]
            if b < 0 or g < 0 or r < 0 or b > 255 or g > 255 or r > 255:
                p[0], p[1], p[2] = 0, 0, 0
            else:
                p[0], p[1], p[2] = b, g, r
    # for i, r in enumerate(range(r_min, r_max)):
    #     for j, g in enumerate(range(g_min, g_max)):
    #         for k, b in enumerate(range(b_min, b_max)):
    #             p = img[i][j]
    #             p[0], p[1], p[2] = b, g, r

    # cv2.imshow('image', img)
    # cv2.setWindowProperty('image', cv2.WND_PROP_TOPMOST, 1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img


class TestApp(object):

    def __init__(self):



        self.root = simple_image_tk.init_tk("Tk Test")

        # image1 = Image.open("data/cyberpunk.png")
        # image1 = image1.resize((200, 200))
        self.test1 = ImageTk.PhotoImage(file="data/cyberpunk.png")

        # image2 = Image.open('data/futuristic_city.png')


        self.canvas = tk.Canvas(self.root, width=500, height=500, bg='#777777')
        image_container = self.canvas.create_image(0, 0, anchor="nw", image=self.test1)
        # self.canvas.itemconfig(image_container, image=self.test1)
        self.canvas.pack()

        def update_image(r, g):
            b = 100
            radius = 150
            self.img = gradient(r, g, b, radius)
            self.test2 = ImageTk.PhotoImage(Image.fromarray(self.img))
            self.image_container = self.canvas.create_image(0, 0, anchor="nw", image=self.test2)
            # self.canvas.itemconfig(self.image_container, image=self.test2)

        self.r = 0
        def update(r):
            r_new = int(float(r))
            if r_new == self.r:
                return
            self.r = r_new
            update_image(self.r, self.r)

        self.scale = ttk.Scale(self.root, from_=70, to=185, length=1000, command=update)
        self.scale.pack()
        # button = ttk.Button(self.root, text="Update", command=lambda: update())
        # button.pack()




    def run(self):
        try:
            self.root.mainloop()
        finally:
            SimpleImage.close_windows()


def main():
    r, g, b = 100, 150, 100
    radius = 200
    img = gradient(r, g, b, radius)
    app = TestApp()
    app.run()



if __name__ == '__main__':
    main()