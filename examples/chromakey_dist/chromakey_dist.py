import math
from simple_image import SimpleImage, SimpleColor


def copy_color(pix1, pix2):
    pix1.r = pix2.r
    pix1.g = pix2.g
    pix1.b = pix2.b


def replace_background_green(img, img_bg):
    for pix in img:
        if pix.g > (pix.b + pix.r):
            pix_bg = img_bg.get_pixel(pix.x, pix.y)
            copy_color(pix, pix_bg)
    return img


def replace_background_blue(img, img_bg):
    for pix in img:
        if pix.b > (pix.g + pix.r):
            pix_bg = img_bg.get_pixel(pix.x, pix.y)
            copy_color(pix, pix_bg)
    return img


def color_distance(c1, c2):
    dr = c2.r - c1.r
    dg = c2.g - c1.g
    db = c2.b - c1.b
    dist = math.sqrt((dr*dr) + (dg*dg) + (db*db))
    return dist


def replace_background(img, img_bg, color_bg, dist_max=170):
    for pix in img:
        dist = color_distance(pix, color_bg)
        if dist < dist_max:
            pix_bg = img_bg.get_pixel(pix.x, pix.y)
            copy_color(pix, pix_bg)
    return img


def main():
    img_ck = SimpleImage('data/girl_black_dress_bs.png')

    img_bg = SimpleImage('data/futuristic_city.png')
    img_bg.resize_proportional(height=img_ck.height)

    color_bg = SimpleColor(67, 119, 236)
    img_ck = img_ck.copy().add_border_centered(img_bg.width, img_bg.height, color_bg)

    dist_max = 130
    img = replace_background(img_ck.copy(), img_bg, color_bg, dist_max)

    img_ck.put_in_window('chroma key')
    img.put_in_window('composited')

    SimpleImage.show_windows()


if __name__ == '__main__':
    main()
