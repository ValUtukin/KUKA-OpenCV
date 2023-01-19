import numpy as np
import cv2 as cv
from find_kuka_points import rescale_frame


def undistort_image(img):
    h, w = img.shape[:2]
    map1, map2 = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv.CV_16SC2)
    undistorted_img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
    return undistorted_img


DIM = (1280, 720)
K = np.array(
        [[1400.5312752987763, 0.0, 628.4219705806136], [0.0, 1408.6956871650618, 414.91973942826155], [0.0, 0.0, 1.0]])
D = np.array([[-0.147852348788544], [0.7021442092673658], [-3.4442108779354763], [0.608256797813276]])

if __name__ == '__main__':
    DIM = (1280, 720)
    K = np.array(
        [[1400.5312752987763, 0.0, 628.4219705806136], [0.0, 1408.6956871650618, 414.91973942826155], [0.0, 0.0, 1.0]])
    D = np.array([[-0.147852348788544], [0.7021442092673658], [-3.4442108779354763], [0.608256797813276]])
    image = cv.imread('../fishEye/WIN_20230113_14_45_34_Pro.jpg')
    rescale = rescale_frame(image, scale=0.5)
    cv.imshow('Orig', image)
    undistort_image(image)
    cv.waitKey(0)
