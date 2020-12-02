import cv2 as cv
import numpy as np


class tracking:
    # Constant
    window_capture_trackbar  = "Trackbars"
    max_value = 255
    max_value_H = 179
    low_H = 0
    low_S = 0
    low_V = 0
    high_H = 0
    high_S = 0
    high_V = 0
    low_H_name = 'Low H'
    low_S_name = 'Low S'
    low_V_name = 'Low V'
    high_H_name = 'High H'
    high_S_name = 'High S'
    high_V_name = 'High V'

    # Properties
    needle_img = None
    needle_width = 0
    needle_height = 0
    method = None

    # Constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)   # Load image we are trying to match

        # Read image width and height
        self.needle_width = self.needle_img.shape[1]
        self.needle_height = self.needle_img.shape[0]

        # Methods: Different Object Detection methods: https://docs.opencv.org/4.0.1/df/dfb/group__imgproc__object.html#ga3a7850640f1fe1f58fe91a2d7583695d
        self.method = method    # Change in methods through constructor above. 

    def find_pos(self, haystack_img, threshold=0.5):
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
        return rectangles

    # Pass (x, y, w, h) params to draw rectangles: Reference ObjectTracking_Webcam.py file  
    def draw_rectangles(self, haystack_img, rectangles):
        # https://docs.opencv.org/master/d6/d6e/group__imgproc__draw.html#gaf076ef45de481ac96e0ab3dc2c29a777
        line_color = (0, 0, 255)    # BGR color, 0,0,255 for red box
        line_type = cv.LINE_4       # Line type 4 = 4 connected lines
        # (X, Y) is the location to draw the box
        # (W, H) is width and height X + Width and Y + Height to draw the full box
        for (x, y, w, h) in rectangles:     # Box pos
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType = line_type)    # Draw box
        return haystack_img

    # Create GUI window with controls for adjusting color conversion in real-time: code copied from OpenCV tutorial for threshold inRange:
    # https://docs.opencv.org/4.2.0/da/d97/tutorial_threshold_inRange.html
    def init_control_gui(self):
        cv.namedWindow(self.window_capture_trackbar, cv.WINDOW_NORMAL)  # Create window to display the default frame and threshold frame
        cv.resizeWindow(self.window_capture_trackbar, 400, 400)         # Resize window

        # cv.createTrackbar requires a callback to update params
        # This is not needed in this case because we will be using getTrackbarPos() instead
        def nothing(position):  # Because this is not a optional parameter we use a function to skip pass it
            pass

        # Create trackbars to set range of HSV values
        # OpenCV scale for HSV: H=0-179, S=0-255, V=0-255
        cv.createTrackbar(self.low_H_name, self.window_capture_trackbar , self.low_H, self.max_value_H, nothing)
        cv.createTrackbar(self.low_S_name, self.window_capture_trackbar , self.low_S, self.max_value, nothing)
        cv.createTrackbar(self.low_V_name, self.window_capture_trackbar , self.low_V, self.max_value, nothing)

        cv.createTrackbar(self.high_H_name, self.window_capture_trackbar , self.high_H, self.max_value_H, nothing)
        cv.createTrackbar(self.high_S_name, self.window_capture_trackbar , self.high_S, self.max_value, nothing)
        cv.createTrackbar(self.high_V_name, self.window_capture_trackbar , self.high_V, self.max_value, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos(self.high_H_name, self.window_capture_trackbar, self.max_value_H)
        cv.setTrackbarPos(self.high_S_name, self.window_capture_trackbar, self.max_value)
        cv.setTrackbarPos(self.high_V_name, self.window_capture_trackbar, self.max_value)
        # Trackbar for increasing and decreasing saturation and value
        cv.createTrackbar('Sat_add', self.window_capture_trackbar , 0, self.max_value, nothing)
        cv.createTrackbar('Sat_sub', self.window_capture_trackbar , 0, self.max_value, nothing)
        cv.createTrackbar('Value_add', self.window_capture_trackbar , 0, self.max_value, nothing)
        cv.createTrackbar('Value_sub', self.window_capture_trackbar , 0, self.max_value, nothing)
