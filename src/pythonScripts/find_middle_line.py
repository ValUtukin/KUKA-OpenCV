import math
import cv2 as cv
import camera_actions as camera
import find_contours as fc


def get_points_till_first_edge(points):
    first_edge_center_pixel_coords = []
    first_edge_left_pixel_coords = []
    first_edge_right_pixel_coords = []
    for i in range(0, len(points)):
        first_edge_left_pixel_coords.append([points[i][0], points[i][1]])
        r0 = 15
        J = -1
        for j in range(i + 1, len(points)):
            r = math.sqrt((points[j][0] - points[i][0]) ** 2 + (points[j][1] - points[i][1]) ** 2)
            if (r < 15) and (abs(i - j) >= 20) and (abs(i - j) <= len(points) - 20) and r < r0:
                J = j
                r0 = r
                xc = int((points[j][0] + points[i][0]) / 2)
                yc = int((points[j][1] + points[i][1]) / 2)
                first_edge_center_pixel_coords.append([xc, yc])
                first_edge_right_pixel_coords.append([points[j][0], points[j][1]])
        if J < 0:
            break  # find an edge
        else:
            continue
    return first_edge_left_pixel_coords, first_edge_center_pixel_coords, first_edge_right_pixel_coords


def get_points_till_second_edge(points):
    second_edge_left_pixel_coords = []
    second_edge_center_pixel_coords = []
    second_edge_right_pixel_coords = []
    for i in range(len(points) - 1, 0, -1):
        second_edge_left_pixel_coords.append([points[i][0], points[i][1]])
        r0 = 15
        J = -1
        for j in range(i, 0, -1):
            r = math.sqrt((points[j][0] - points[i][0]) ** 2 + (points[j][1] - points[i][1]) ** 2)
            if (r < 15) and (abs(i - j) >= 20) and (abs(i - j) <= len(points) - 20) and r < r0:
                J = j
                r0 = r
                xc = int((points[j][0] + points[i][0]) / 2)
                yc = int((points[j][1] + points[i][1]) / 2)
                second_edge_center_pixel_coords.append([xc, yc])
                second_edge_right_pixel_coords.append([points[j][0], points[j][1]])
        if J < 0:
            break  # find an edge
        else:
            continue
    return second_edge_left_pixel_coords, second_edge_center_pixel_coords, second_edge_right_pixel_coords


def get_all_points(till_first_edge, till_second_edge):
    return till_first_edge[::-1] + till_second_edge  # inside returned list might be duplicates


def draw_line(blank, points, color=(0, 255, 0)):
    for i in range(0, len(points)):
        cv.circle(blank, (points[i][0], points[i][1]), 1, color, thickness=1)
    cv.imshow('Middle line', blank)


def no_duplicate(points):  # remove duplicates from given list
    result = []
    for point in points:
        if point not in result:
            result.append(point)
    return result


def main():
    img = cv.imread('../../images/testCurve.jpg')
    undistorted_img = camera.undistort_fisheye(img)
    gray = cv.cvtColor(undistorted_img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, ksize=(5, 5), sigmaX=1)
    canny = cv.Canny(blur, 30, 60, apertureSize=3, L2gradient=True)
    contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    points = fc.find_coord(contours[0])

    first_points = get_points_till_first_edge(points)
    second_points = get_points_till_second_edge(points)
    all_points = get_all_points(first_points, second_points)
    no_dp_points = no_duplicate(all_points)

    print(f'Total amount of points in the middle line is {len(first_points[::-1] + second_points)}')
    print(f'Amount of points till first edge is {len(first_points)}')
    print(f'Amount of points till second edge is {len(second_points)}')
    print('All points below:')
    print(*no_dp_points)
    draw_line(undistorted_img, no_dp_points)

    cv.waitKey(0)


if __name__ == "__main__":
    main()
