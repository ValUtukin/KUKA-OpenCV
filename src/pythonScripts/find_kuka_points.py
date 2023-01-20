import cv2 as cv
import find_middle_line as fml
from find_contours import find_coord


def kuka_coord(points):
    kuka_points = []
    for point in points:
        x = 240.8 + 90.56 - (point[1] - 720/2) / 5.08
        y = 325.38 - 5.19 - (point[0] - 1280/2) / 5.08
        kuka_points.append([round(x, 2), round(y, 2)])
    return kuka_points


def main():
    img = cv.imread('../../images/1.jpg')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 1)
    canny = cv.Canny(blur, 30, 60, apertureSize=3, L2gradient=True)
    contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    pixel_coord = find_coord(contours[0])

    till_first_edge = fml.get_points_till_first_edge(pixel_coord)
    till_second_edge = fml.get_points_till_second_edge(pixel_coord)

    pixel_middle_line = fml.get_all_middle_points(till_first_edge, till_second_edge)
    fml.draw_middle_line(img, pixel_middle_line)

    kuka_middle_line = kuka_coord(pixel_middle_line)

    print(len(kuka_middle_line))
    print(*kuka_coord(kuka_middle_line))
    cv.waitKey(0)


if __name__ == '__main__':
    main()
