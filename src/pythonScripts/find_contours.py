import cv2 as cv
import numpy as np
import os


# Method for saving images in specific directory
def save_image(file_name, image, dir_name):
    os.chdir(dir_name)
    cv.imwrite(file_name, image)


def save_all_contours(contours, dir_name=r'C:\Users\Bogh\TestFolder'):
    pass


#  Find coord
def find_coord(contour):
    points = list()
    for point in contour:
        points.append([point[0][0], point[0][1]])  # Saving points as (x;y)
    return points


def find_longest_contour(contours):
    longest_contour = None
    longest_contour_length = 0
    for i in range(0, len(contours)):
        if len(contours[i]) > longest_contour_length:
            longest_contour = contours[i]
            longest_contour_length = len(contours[i])
    return longest_contour


def draw_all_contours(contours, hierarchy, blank, color=(0, 255, 0)):
    for i in range(0, len(contours)):
        cv.drawContours(blank, contours, i, color, 1, cv.LINE_8, hierarchy, 0)
    cv.imshow('All contours', blank)


def main():
    img = cv.imread('../../images/testCurve.jpg')
    cropped_img = img[25:, :-20]  # Remove unwanted borders for exact image 'Images/lines_original.jpg'
    gray = cv.cvtColor(cropped_img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 1)
    canny = cv.Canny(blur, 30, 60, apertureSize=3, L2gradient=True)

    contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)  # Find contours (canny)
    drawing = np.zeros((canny.shape[0], canny.shape[1], 1), dtype='uint8')  # Make Matrix for drawing
    # terminate_matrix = drawing.copy()
    directory = r'C:\Users\Bogh\TestFolder'  # Directory for saving contours

    for i in range(len(contours)):
        if len(contours[i]):  # If contour has more than 10 points
            cv.drawContours(drawing, contours, i, 255, 1, cv.LINE_8, hierarchy, 0)  # Draw contour in drawing matrix

            # contour = cv.bitwise_xor(drawing, terminate_matrix)
            # save_image(f'Contour#{i + 1}.jpg', contour, directory)  # Saving .jpg's of contours

            # terminate_matrix = cv.bitwise_or(contour, terminate_matrix)  # Add contour to terminate matrix
    cv.imshow('Contours', drawing)
    print(len(contours))
    points = find_coord(contours[2])  # Get a list of coord of contour index 2
    print(*points, sep="\n")
    cv.waitKey(0)


if __name__ == '__main__':
    main()
