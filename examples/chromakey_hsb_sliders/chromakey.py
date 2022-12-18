import numpy as np
import cv2 as cv
from simple_image import SimpleImage


def run(img, img_bg, img_hsv, hsv_lower, hsv_upper):
    mask_bg = cv.inRange(img_hsv, hsv_lower, hsv_upper)
    mask_fg = cv.bitwise_not(mask_bg)
    res_fg = cv.bitwise_and(img, img, mask=mask_fg)
    res_bg = cv.bitwise_and(img_bg, img_bg, mask=mask_bg)
    res = cv.bitwise_or(res_bg, res_fg)
    return res


def main():
    img = cv.imread('data/girl_shadows_gs.png')
    img_bg = cv.imread('data/cyberpunk.png')
    img_bg = cv.resize(img_bg, (img.shape[1], img.shape[0]))
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv_lower = np.array([50, 122, 100])
    hsv_upper = np.array([80, 255, 255])

    res = run(img, img_bg, img_hsv, hsv_lower, hsv_upper)
    si_img = SimpleImage.from_image_data(img, mode='BGR')
    si_img.show('Chroma Screen')
    si_res = SimpleImage.from_image_data(res, mode='BGR')
    window = si_res.show('Result')
    window.move(482, 0)

    SimpleImage.run()


if __name__ == "__main__":
    main()
