import math
from simple_image import SimpleImage, SimpleColor


def color_distance(c1, c2):
    dr = c2.r - c1.r
    dg = c2.g - c1.g
    db = c2.b - c1.b
    dist = math.sqrt((dr*dr) + (dg*dg) + (db*db))
    return dist


def mask_color_with_distance(img, color, dist_max=170):
    for p in img:
        dist = color_distance(p, color)
        if dist < dist_max:
            p.r = p.g = p.b = 0
    return img


def main():
    img = SimpleImage('data/ball_pit.png')
    dist_max = 50
    color = SimpleColor(175, 137, 0)
    img_masked = mask_color_with_distance(img.copy(), color, dist_max)

    img_masked.show('masked')

    SimpleImage.wait_key_and_close_windows(delay=120)


if __name__ == '__main__':
    main()
