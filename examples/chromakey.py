import numpy as np
import cv2 as cv


def main():
    img = cv.imread('data/girl_shadows_gs.png')
    img_bg = cv.imread('data/cyberpunk.png')
    img_bg = cv.resize(img_bg, (img.shape[1], img.shape[0]))

    lower_hsv = np.array([50, 122, 0])
    upper_hsv = np.array([80, 255, 255])
    img_hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    mask_bg = cv.inRange(img_hsv, lower_hsv, upper_hsv)
    mask_fg = cv.bitwise_not(mask_bg)

    res_fg = cv.bitwise_and(img, img, mask= mask_fg)
    res_bg = cv.bitwise_and(img_bg, img_bg, mask= mask_bg)
    res = cv.bitwise_or(res_bg, res_fg)

    cv.imshow('chroma key', img)
    cv.setWindowProperty('chroma key', cv.WND_PROP_TOPMOST, 1)

    cv.imshow('composited', res)
    cv.setWindowProperty('composited', cv.WND_PROP_TOPMOST, 0)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
