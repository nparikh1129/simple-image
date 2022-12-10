import cv2 as cv
from simple_image import SimpleImage



def main():
    simp_img = SimpleImage('data/fire_breather.png')

    img = simp_img.image_data
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)
    simp_img.image_data = img

    simp_img.show('grayscale')
    SimpleImage.wait_key_and_close_windows()


if __name__ == '__main__':
    main()
