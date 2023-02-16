import time
import cv2 as cv
import find_middle_line as fml
import camera_actions as camera
import find_contours as fc


def kuka_coord(points):
    kuka_points = []
    for point in points:
        x = 240.82 + 78.97 + 1.1 - (point[1] - 720/2) / 4.8
        y = 325.38 - 10.32 + 0.9 - (point[0] - 1280/2) / 4.8
        kuka_points.append([round(x, 2), round(y, 2)])
    return kuka_points


def main():
    time.sleep(2.0)
    capture = cv.VideoCapture(0)
    capture.set(3, 1280)
    capture.set(4, 720)
    frame = camera.grab_frame_from_camera(capture)

    if type(frame) is str:
        print('Cannot get a frame')
    else:
        undistorted = camera.undistort_fisheye(frame)
        gray = cv.cvtColor(undistorted, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (5, 5), 1)
        canny = cv.Canny(blur, 30, 60, apertureSize=3, L2gradient=True)
        contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        longest_contour = fc.find_longest_contour(contours)
        pixel_coord = fc.find_coord(longest_contour)

        fel, fec, fer = fml.get_points_till_first_edge(pixel_coord)
        sel, sec, ser = fml.get_points_till_second_edge(pixel_coord)

        pixel_left_line = fml.get_all_points(fel, sel)
        pixel_middle_line = fml.get_all_points(fec, sec)
        pixel_right_line = fml.get_all_points(fer, ser)

        no_dp_points = fml.no_duplicate(pixel_middle_line)
        skip_duplicate = [no_dp_points[i] for i in range(0, len(no_dp_points), 3)]

        kuka_middle_line = kuka_coord(skip_duplicate)

        print(f'Total amount of points for KUKA:{len(kuka_middle_line)}')
        return kuka_middle_line


if __name__ == '__main__':
    main()
