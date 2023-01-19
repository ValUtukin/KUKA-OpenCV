import cv2 as cv
import numpy as np
from find_edges import canny_edge_detection


def undistort_image(img):
    DIM = (1280, 720)
    K = np.array(
        [[1400.5312752987763, 0.0, 628.4219705806136], [0.0, 1408.6956871650618, 414.91973942826155], [0.0, 0.0, 1.0]])
    D = np.array([[-0.147852348788544], [0.7021442092673658], [-3.4442108779354763], [0.608256797813276]])
    h, w = img.shape[:2]
    map1, map2 = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv.CV_16SC2)
    undistorted_img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)
    return undistorted_img


img = cv.imread('../images/test_photo1.jpg')
undis = undistort_image(img)

canny = canny_edge_detection(undis, ksize=(5, 5), threshold1=30, threshold2=60)
contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

drawing = np.zeros((canny.shape[0], canny.shape[1], 1), dtype='uint8')  # Make Matrix for drawing
terminate_matrix = drawing.copy()
directory = r'C:\Users\Bogh\TestFolder'
print(len(contours))
for i in range(len(contours)):
    if len(contours[i]) > 200:  # If contour has more than 10 points
        cv.drawContours(drawing, contours, i, 255, 1, cv.LINE_8, hierarchy, 0)  # Draw contour in drawing matrix

        contour = cv.bitwise_xor(drawing, terminate_matrix)
        cv.imwrite(f'Contour#{i + 1}.jpg', contour)  # Saving .jpg's of contours

        terminate_matrix = cv.bitwise_or(contour, terminate_matrix)
cv.waitKey(0)
