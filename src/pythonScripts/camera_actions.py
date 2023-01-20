import cv2 as cv
import numpy as np


def undistort_fisheye(img):
    DIM = (1280, 720)
    K = np.array(
        [[1400.5312752987763, 0.0, 628.4219705806136], [0.0, 1408.6956871650618, 414.91973942826155], [0.0, 0.0, 1.0]])
    D = np.array([[-0.147852348788544], [0.7021442092673658], [-3.4442108779354763], [0.608256797813276]])
    h, w = img.shape[:2]
    map1, map2 = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv.CV_16SC2)
    undistorted_img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
    return undistorted_img


def draw_image_center(image):
    center_points = []
    if image.shape[1] % 2 != 0:
        center_pixel_x = (image.shape[1] // 2) + 1
        if image.shape[0] % 2 != 0:
            center_pixel_y = (image.shape[0] // 2) + 1
            center_points.append([center_pixel_x, center_pixel_y])
        else:
            center_pixel_y = [image.shape[0] // 2, (image.shape[0] // 2) + 1]
            center_points.append([center_pixel_x, center_pixel_y[0]])
            center_points.append([center_pixel_x, center_pixel_y[1]])
    else:
        center_pixel_x = [image.shape[1] // 2, (image.shape[1] // 2) + 1]
        if image.shape[0] % 2 != 0:
            center_pixel_y = (image.shape[0] // 2) + 1
            center_points.append([center_pixel_x[0], center_pixel_y])
            center_points.append([center_pixel_x[1], center_pixel_y])
        else:
            center_pixel_y = [image.shape[0] // 2, (image.shape[0] // 2) + 1]
            center_points.append([center_pixel_x[0], center_pixel_y[0]])
            center_points.append([center_pixel_x[0], center_pixel_y[1]])
            center_points.append([center_pixel_x[1], center_pixel_y[0]])
            center_points.append([center_pixel_x[1], center_pixel_y[1]])
    for point in center_points:
        cv.circle(image, (point[0], point[1]), 1, (0, 0, 255), thickness=2)
    return center_points, image


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


def main():
    img = cv.imread('../../images/oddCurve.png')
    fish_eye = cv.imread('../../images/Apoint.jpg')
    undistorted_img = undistort_fisheye(fish_eye)
    center, new_image = draw_image_center(img)
    print(*center)
    cv.imshow('Center', new_image)
    cv.imshow('Undistorted', undistorted_img)
    cv.waitKey(0)


if __name__ == "__main__":
    main()
