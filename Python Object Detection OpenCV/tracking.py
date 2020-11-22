import cv2 as cv
import numpy as np


class tracking:

    # properties
    needle_img = None
    needle_width = 0
    needle_height = 0
    method = None

    # constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)   # Load image we are trying to match

        # Read image width and height
        self.needle_width = self.needle_img.shape[1]
        self.needle_height = self.needle_img.shape[0]

        # Methods: Different Object Detection methods: https://docs.opencv.org/4.0.1/df/dfb/group__imgproc__object.html#ga3a7850640f1fe1f58fe91a2d7583695d
        self.method = method    # Change in methods through constructor above. 

    def find_pos(self, haystack_img, threshold=0.5, debug_mode=None):
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)       # Run algorithm
        
        locations = np.where(result >= threshold)                                   # Get position from match results
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_width, self.needle_height]
            rectangles.append(rect)
            rectangles.append(rect)
            
        # Group rectangles so they combine to similar size and location, otherwise the rectangle will be thick
        # https://docs.opencv.org/3.4/d5/d54/group__objdetect.html
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5) 
        points = []
        if len(rectangles):

            line_color = (0, 255, 0)
            line_type = cv.LINE_4

            for (x, y, w, h) in rectangles:

                center_x = x + int(w/2)
                center_y = y + int(h/2)

                points.append((center_x, center_y))

                top_left = (x, y)
                bottom_right = (x + w, y + h)

                cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                            lineType=line_type, thickness=2)

        if debug_mode:
            cv.imshow('Matches', haystack_img)

        return points