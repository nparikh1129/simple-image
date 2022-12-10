from simple_image import SimpleImage


def color_balance(img):
    r_factor = 0.333/0.299
    g_factor = 0.333/0.587
    b_factor = 0.333/0.114
    for p in img:
        p.r = min(255, int(p.r * r_factor))
        p.g = int(p.g * g_factor)
        p.b = min(255, int(p.b * b_factor))
    return img


def main():
    img = SimpleImage('data/rgb_spectrum.png')
    img_cb = color_balance(img.copy())

    img.show('image')
    img_cb.show('color balanced')

    SimpleImage.wait_key_and_close_windows()


if __name__ == '__main__':
    main()
