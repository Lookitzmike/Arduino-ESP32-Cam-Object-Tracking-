# This program is from https://docs.opencv.org/master/d4/dc6/tutorial_py_template_matching.html
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread(r'C:\Users\ML\Documents\GitHub\Arduino-ESP32-Cam-Object-Tracking-\Python Object Detection OpenCV\Python Testing Files\inu.jpg', 0)           # OG
img2 = img.copy()                   # compare
template = cv.imread(r'C:\Users\ML\Documents\GitHub\Arduino-ESP32-Cam-Object-Tracking-\Python Object Detection OpenCV\Python Testing Files\inu_face.jpg', 0) # detect
w, h = template.shape[::-1]

# All 6 methods 
methods = ['cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED']

for x in methods:
    img = img2.copy()
    method = eval(x)
    # Apply methods
    res = cv.matchTemplate(img, template, method)
    # https://docs.opencv.org/master/d2/de8/group__core__array.html#ga8873b86a29c5af51cafdcee82f8150a7
    min_val, max_val, min_loc, max_loc, = cv.minMaxLoc(res)
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:       # if method is this then take minimum
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img, top_left, bottom_right, 255, 2)
    plt.subplot(121), plt.imshow(res, cmap='gray')
    plt.title('Matching'), plt.xticks([]), plt.yticks([])
    plt.subplot( 122), plt.imshow(img, cmap= 'gray')
    plt.title('Detect'), plt.xticks([]), plt.yticks([])
    plt.suptitle(x)
    plt.show()
