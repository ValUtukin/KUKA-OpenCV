import cv2 as cv
import numpy as np
import os
import math
from find_edges import canny_edge_detection
from find_contours import find_coord


def save_image(file_name, image, dir_name):
    os.chdir(dir_name)
    cv.imwrite(file_name, image)


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


def rescale_frame(img, scale=0.5):
    # Work for images, video and live video
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(img, dimensions, interpolation=cv.INTER_AREA)


def kuka_coord(points):
    kuka_points = []
    for point in points:
        x = 232.72 + (810 - int(point[1])) * 0.543
        y = 199.49 + (560 - int(point[0])) * 0.543
        kuka_points.append([round(x, 2), round(y, 2)])
    return kuka_points


def main():
    # capture = cv.VideoCapture(0)
    # capture.set(3, 1280)
    # capture.set(4, 720)
    # frame = grab_frame_from_camera(capture)
    img = cv.imread('../images/test_photo1.jpg')
    undis = undistort_image(img)

    if undis.shape[1] % 2 != 0:  # find x coord of the center of the image
        center_pixel_x = [(undis.shape[1] // 2) + 1]
    else:
        center_pixel_x = [undis.shape[1] // 2, (undis.shape[1] // 2) + 1]

    if undis.shape[0] % 2 != 0:  # find x coord of the center of the image
        center_pixel_y = [(undis.shape[0] // 2) + 1]
    else:
        center_pixel_y = [undis.shape[0] // 2, (undis.shape[0] // 2) + 1]
    if len(center_pixel_x) > 1 and len(center_pixel_y) > 1:  # Четная длина и ширина
        cv.circle(undis, (center_pixel_x[0], center_pixel_y[0]), 1, (0, 0, 255), thickness=1)
        cv.circle(undis, (center_pixel_x[1], center_pixel_y[0]), 1, (0, 0, 255), thickness=1)
        cv.circle(undis, (center_pixel_x[0], center_pixel_y[1]), 1, (0, 0, 255), thickness=1)
        cv.circle(undis, (center_pixel_x[1], center_pixel_y[1]), 1, (0, 0, 255), thickness=1)
    # cv.imshow('Image', img)
    # undistorted_img = undistort_image(img)
    # cv.imshow('UnImage', undistorted_img)
    # cv.imwrite('Image1.jpg', undistorted_img)
    # cropped_img = undistorted_img[150:710, 255:1065]

    canny = canny_edge_detection(undis, ksize=(5, 5), threshold1=30, threshold2=60)
    contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    print(len(contours))
    most_bigger_contour = 0
    for i in range(0, len(contours)):
        if len(contours[i]) > most_bigger_contour:
            most_bigger_contour = i
        else:
            continue
    print(len(contours[46]))
    points = []
    for point in contours[most_bigger_contour]:
        points.append([point[0][0], point[0][1]])

    points_copy = points.copy()
    first_edge_center_pixel_coords = []
    second_edge_center_pixel_coords = []

    for i in range(0, len(points)):  # Начинаем цикл
        r0 = 15
        J = -1
        for j in range(i + 1, len(points)):  # Бежим по остальным точкам и ищем соседа
            r = math.sqrt((points[j][0] - points[i][0]) ** 2 + (points[j][1] - points[i][1]) ** 2)  # считаем разницу
            if (r < 10) and (abs(i - j) >= 15) and (abs(i - j) <= len(points) - 15) and r < r0:
                J = j
                r0 = r

                xc = int((points[j][0] + points[i][0]) / 2)
                yc = int((points[j][1] + points[i][1]) / 2)
                first_edge_center_pixel_coords.append([xc, yc])

                cv.circle(undis, (xc, yc), 1, (255, 0, 255), thickness=1)
        print(f'i = {i}, j = {J}, r = {r0}')  # строчка для отладки
        if J < 0:
            print('edge')
            break
        else:
            continue

    for i in range(len(points) - 1, 0, -1):  # Начинаем цикл
        r0 = 15
        J = -1
        for j in range(i, 0, -1):  # Бежим по остальным точкам и ищем соседа
            r = math.sqrt((points[j][0] - points[i][0]) ** 2 + (points[j][1] - points[i][1]) ** 2)  # считаем разницу
            if (r < 11) and (abs(i - j) >= 15) and (abs(i - j) <= len(points) - 15) and r < r0:
                J = j
                r0 = r

                xc = int((points[j][0] + points[i][0]) / 2)
                yc = int((points[j][1] + points[i][1]) / 2)
                second_edge_center_pixel_coords.append([xc, yc])

                cv.circle(undis, (xc, yc), 1, (0, 255, 255), thickness=1)
        print(f'i = {i}, j = {J}, r = {r0}')  # строчка для отладки
        if J < 0:
            print('edge')
            break
        else:
            continue

    center_pixel_coords = first_edge_center_pixel_coords[::-1] + second_edge_center_pixel_coords

    # print(len(center_pixel_coords))
    # return kuka_coord(center_pixel_coords)
    cv.imshow('Image', undis)
    cv.waitKey(0)


if __name__ == '__main__':
    main()
