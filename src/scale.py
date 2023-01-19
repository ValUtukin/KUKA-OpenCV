import cv2 as cv
import numpy as np


def undistort_image(img):
    DIM = (1280, 720)
    K = np.array(
        [[1400.5312752987763, 0.0, 628.4219705806136], [0.0, 1408.6956871650618, 414.91973942826155], [0.0, 0.0, 1.0]])
    D = np.array([[-0.147852348788544], [0.7021442092673658], [-3.4442108779354763], [0.608256797813276]])
    h, w = img.shape[:2]
    map1, map2 = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv.CV_16SC2)
    undistorted_img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
    return undistorted_img


def grab_frame_from_camera(video_capture):
    i = 0
    if video_capture.isOpened():
        while i < 10:
            ret, img = video_capture.read()
            if ret:
                return img
            else:
                i += 1
                continue
        else:
            return "cannot get a frame"
    else:
        return "cannot open camera"


img = cv.imread('../images/Apoint.jpg')
undistorted_img = undistort_image(img)

if undistorted_img.shape[1] % 2 != 0:  # find x coord of the center of the image
    center_pixel_x = [(undistorted_img.shape[1] // 2) + 1]
else:
    center_pixel_x = [undistorted_img.shape[1] // 2, (undistorted_img.shape[1] // 2) + 1]

if undistorted_img.shape[0] % 2 != 0:  # find x coord of the center of the image
    center_pixel_y = [(undistorted_img.shape[0] // 2) + 1]
else:
    center_pixel_y = [undistorted_img.shape[0] // 2, (undistorted_img.shape[0] // 2) + 1]

if len(center_pixel_x) > 1 and len(center_pixel_y) > 1: # Четная длина и ширина
    cv.circle(undistorted_img, (center_pixel_x[0], center_pixel_y[0]), 1, (0, 0, 255), thickness=1)
    cv.circle(undistorted_img, (center_pixel_x[1], center_pixel_y[0]), 1, (0, 0, 255), thickness=1)
    cv.circle(undistorted_img, (center_pixel_x[0], center_pixel_y[1]), 1, (0, 0, 255), thickness=1)
    cv.circle(undistorted_img, (center_pixel_x[1], center_pixel_y[1]), 1, (0, 0, 255), thickness=1)
cv.imshow('Frame', undistorted_img)
cv.imwrite('Frame_with_center.jpg', undistorted_img)
cv.waitKey(0)
