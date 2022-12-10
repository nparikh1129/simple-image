from simple_image import SimpleImage


def main():
    img = SimpleImage('data/t-rex.png')
    img.show('rot')
    SimpleImage.wait_key_and_close_windows()


if __name__ == '__main__':
    main()
