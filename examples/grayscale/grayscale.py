import numpy as np
import cv2 as cv
from simple_image import SimpleImage


def lightness(img):
    for pix in img:
        val_max = max(pix.r, pix.g, pix.b)
        val_min = min(pix.r, pix.g, pix.b)
        lum = (val_max + val_min) / 2
        pix.r = pix.g = pix.b = lum
    return img


def intensity(img):
    for pix in img:
        val = (pix.r + pix.g + pix.b) / 3
        pix.r = pix.g = pix.b = val
    return img


def luma601(img):
    for pix in img:
        val = 0.299*pix.r + 0.587*pix.g + 0.114*pix.b
        pix.r = pix.g = pix.b = int(val)
    return img


"""
https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html#color_convert_rgb_lab
"""
def cielab_lightness(img):
    bgr = img.image_data
    lab = cv.cvtColor(bgr, cv.COLOR_RGB2LAB)
    l, a, b = cv.split(lab)
    a = np.full(l.shape, 128, dtype=np.uint8)
    b = np.full(l.shape, 128, dtype=np.uint8)
    lab = cv.merge((l, a, b))
    gs = cv.cvtColor(lab, cv.COLOR_LAB2RGB)
    img_gs = SimpleImage.from_image_data(gs)
    return img_gs


def main():
    img = SimpleImage('data/fire_breather.png')
    img_gs_lum = lightness(img.copy())
    img_gs_avg = intensity(img.copy())
    img_gs_weighted_avg = luma601(img.copy())
    img_gs_lab_l = cielab_lightness(img.copy())

    img.show('original')
    img_gs_lum.show('luminosity').move(640, 0)
    img_gs_avg.show('average').move(0, 498)
    img_gs_weighted_avg.show('weighted average').move(640, 498)
    img_gs_lab_l.show('image')

    SimpleImage.run()


if __name__ == '__main__':
    main()
