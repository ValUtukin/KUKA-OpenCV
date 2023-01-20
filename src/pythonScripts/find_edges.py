import cv2 as cv
import numpy as np


def canny_edge_detection(img, ksize=(3, 3), threshold1=30, threshold2=60):
    gray_wo_blur = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gauss_blur = cv.GaussianBlur(gray_wo_blur, ksize, sigmaX=1, sigmaY=1)
    canny = cv.Canny(gauss_blur, threshold1, threshold2, apertureSize=3, L2gradient=True)
    return canny


def laplacian_edge_detection(img, ksize=5, thresh=4, maxvalue=255):
    median = cv.medianBlur(img, ksize)
    gray_with_blur = cv.cvtColor(median, cv.COLOR_BGR2GRAY)
    lap = cv.Laplacian(gray_with_blur, cv.CV_8U)
    lap = np.uint8(np.absolute(lap))
    threshold, thresh = cv.threshold(lap, thresh, maxvalue, cv.THRESH_BINARY)
    return thresh


def main():
    pass


if __name__ == '__main__':
    main()
