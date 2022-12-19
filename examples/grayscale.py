import cv2 as cv
from simple_image import SimpleImage



def main():
    simp_img = SimpleImage('data/fire_breather.png')

    img = simp_img.image_data
    img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    img = cv.cvtColor(img_gray, cv.COLOR_GRAY2RGB)
    simp_img.image_data = img

    simp_img.put_in_window('grayscale')
    SimpleImage.show_windows()


if __name__ == '__main__':
    main()
