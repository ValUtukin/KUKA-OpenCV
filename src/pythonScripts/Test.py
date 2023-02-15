import math
import cv2 as cv
import numpy as np
import find_middle_line as fml
import find_contours as fc
import camera_actions as ca

img = cv.imread('../../images/testCurve.jpg')
undistorted = ca.undistort_fisheye(img)
gray = cv.cvtColor(undistorted, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (5, 5), 1)
canny = cv.Canny(blur, 30, 60, apertureSize=3, L2gradient=True)
contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
longest_contour = fc.find_longest_contour(contours)
pixel_coord = fc.find_coord(longest_contour)

feL, feC, feR = fml.get_points_till_first_edge(pixel_coord)
seL, seC, seR = fml.get_points_till_second_edge(pixel_coord)

fml.draw_line(undistorted, feL, (0, 0, 255))
fml.draw_line(undistorted, feR, (0, 0, 255))

fml.draw_line(undistorted, seL, (0, 255, 0))
fml.draw_line(undistorted, seR, (0, 255, 0))

fml.draw_line(undistorted, feC, (24, 245, 186))
fml.draw_line(undistorted, seC, (24, 245, 186))
cv.waitKey(0)
