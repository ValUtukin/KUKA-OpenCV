import math
import cv2 as cv
import numpy as np


img = cv.imread(filename='Image/Curve3.png')
cv.imshow('Orig img', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, ksize=(5, 5), sigmaX=1)

canny = cv.Canny(blur, 30, 60, apertureSize=3, L2gradient=True)
# cv.imshow('Canny', canny)
drawing = np.zeros((canny.shape[0], canny.shape[1], 1), dtype='uint8')

contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

points = []

for point in contours[0]:
    points.append([point[0][0], point[0][1]])

points_copy = points.copy()
first_edge_center_pixel_coords = []
second_edge_center_pixel_coords = []

for i in range(0, len(points)):  # Начинаем цикл
    r0 = 15
    J = -1
    for j in range(i+1, len(points)):  # Бежим по остальным точкам и ищем соседа
        r = math.sqrt((points[j][0] - points[i][0])**2 + (points[j][1] - points[i][1])**2)  # считаем разницу
        if (r < 11) and (abs(i - j) >= 15) and (abs(i - j) <= len(points) - 15) and r < r0:
            J = j
            r0 = r

            xc = int((points[j][0] + points[i][0])/2)
            yc = int((points[j][1] + points[i][1])/2)
            first_edge_center_pixel_coords.append([xc, yc])
            # points_copy.pop(i)
            # points_copy.pop(j)

            cv.circle(img, (xc, yc), 1, (255, 0, 255), thickness=1)
    print(f'i = {i}, j = {J}, r = {r0}')  # строчка для отладки
    if J < 0:
        print('edge')
        break
    else:
        continue
        # cv.circle(img, (points[i][0], points[i][1]), 1, (0, 0, 255), thickness=2)  # рисуем красный круг на зафиксированной точке (i)
        # cv.circle(img, (points[J][0], points[J][1]), 1, (0, 255, 0), thickness=2)  # рисуем зеленый круг, на соседе (j) красного (i)

for i in range(len(points)-1, 0, -1):  # Начинаем цикл
    r0 = 15
    J = -1
    for j in range(i, 0, -1):  # Бежим по остальным точкам и ищем соседа
        r = math.sqrt((points[j][0] - points[i][0])**2 + (points[j][1] - points[i][1])**2)  # считаем разницу
        if (r < 11) and (abs(i - j) >= 15) and (abs(i - j) <= len(points) - 15) and r < r0:
            J = j
            r0 = r

            xc = int((points[j][0] + points[i][0])/2)
            yc = int((points[j][1] + points[i][1])/2)
            second_edge_center_pixel_coords.append([xc, yc])
            # points_copy.pop(i)
            # points_copy.pop(j)

            cv.circle(img, (xc, yc), 1, (255, 0, 255), thickness=1)
    print(f'i = {i}, j = {J}, r = {r0}')  # строчка для отладки
    if J < 0:
        print('edge')
        break
    else:
        continue
        # cv.circle(img, (points[i][0], points[i][1]), 1, (0, 0, 255), thickness=2)  # рисуем красный круг на зафиксированной точке (i)
        # cv.circle(img, (points[J][0], points[J][1]), 1, (0, 255, 0), thickness=2)  # рисуем зеленый круг, на соседе (j) красного (i)

center_pixel_coords = first_edge_center_pixel_coords[::-1] + second_edge_center_pixel_coords

cv.imshow('New img', img)
# cv.imwrite('Output.png', img)

for point in center_pixel_coords:
    cv.circle(drawing, (point[0], point[1]), 1, (255, 255, 255), thickness=1)
cv.imshow('Center line', drawing)
print(len(points))
print(len(points_copy))
cv.waitKey(0)
