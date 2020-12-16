import cv2 as cv
import numpy as np
import serial
from HSV_filter import HSV_filter

# serialcomm = serial.Serial('COM3', 9600)    # Change port to whatever arduino connected to

class tracking:
    # Constant
    window_capture_trackbar  = "Trackbars"

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

    def find_pos(self, haystack_img, threshold=0.5, max_results=10):
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)       # Run algorithm
        
        locations = np.where(result >= threshold)                                   # Get position from match results
        locations = list(zip(*locations[::-1]))

        if not locations:   # Reshape empty arrays because empty array when concatenating can cause error 
            return np.array([], dtype=np.int32).reshape(0, 4)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_width, self.needle_height]
            rectangles.append(rect)
            rectangles.append(rect)

        # Group rectangles so they combine to similar size and location, otherwise the rectangle will be thick
        # https://docs.opencv.org/3.4/d5/d54/group__objdetect.html
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5) 
        #print(rectangles)

        if len(rectangles) > max_results:       # Can crash program if too many results
            print('Too many results, increase threshold')
            rectangles = rectangles[:max_results]

        return rectangles

    # Pass (x, y, w, h) params to draw rectangles: Reference ObjectTracking_Webcam.py file  
    def draw_rectangles(self, haystack_img, rectangles):
        track_pos_X, track_pos_Y = 0, 0
        # https://docs.opencv.org/master/d6/d6e/group__imgproc__draw.html#gaf076ef45de481ac96e0ab3dc2c29a777
        line_color = (0, 0, 255)    # BGR color, 0,0,255 for red box
        line_type = cv.LINE_4       # Line type 4 = 4 connected lines
        # (X, Y) is the location to draw the box
        # (W, H) is width and height X + Width and Y + Height to draw the full box
        for (x, y, w, h) in rectangles:     # Box pos
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType = line_type)    # Draw box
            track_pos_X = top_left[0]                           # Center pos = 230-240   Moving Right: 0, Moving Left 300
            track_pos_Y = top_left[1]                           # Center pos = 50-60     Moving Up: 0, Moving Down: 100
        print(track_pos_X, track_pos_Y)
        
        """
        This section is currently a work in progress. Running too fast to arduino is not processing/receiving the data
        Data needs to be processed in arduino to get a average position 
        Need to add counter after 200 iterations or 2 seconds it will send 1 number across 
        """

        # if (track_pos_X > 240):     # I'm right Camera needs to turn left
        #     move_Deg = 120
        #     serialcomm.write(str(move_Deg).encode())       
        # # elif (track_pos_Y < 50):   # I'm going up Camera needs to pitch up
        # #     move_Deg = 60
        # #     serialcomm.write(str(move_Deg).encode())  
        # elif (track_pos_X < 230):   # I'm left Camera needs to turn right
        #     move_Deg = 60
        #     serialcomm.write(str(chr(move_Deg)).encode())
        # # elif (track_pos_Y > 60):   # I'm going down Camera needs to pitch down
        # #     move_Deg = 120
        # #     serialcomm.write(str(move_Deg).encode())
        # elif (track_pos_X in range(230, 240)):  # Center
        #     move_Deg = 90
        #     serialcomm.write(str(chr(move_Deg)).encode())
        # # elif (track_pos_Y in range(50, 60)):   # Center
        # #     move_Deg = 90
        # #     serialcomm.write(str(move_Deg).encode())
        # return haystack_img

    # Create GUI window with controls for adjusting color conversion in real-time: code copied from OpenCV tutorial for threshold inRange:
    # https://docs.opencv.org/4.2.0/da/d97/tutorial_threshold_inRange.html
    def init_control_gui(self):
        cv.namedWindow(self.window_capture_trackbar, cv.WINDOW_NORMAL)  # Create window to display the default frame and threshold frame
        cv.resizeWindow(self.window_capture_trackbar, 350, 700)         # Resize window

        # cv.createTrackbar requires a callback to update params
        # This is not needed in this case because we will be using getTrackbarPos() instead
        def nothing(position):  # Because this is not a optional parameter we use a function to skip pass it
            pass

        # Create trackbars to set range of HSV values
        # OpenCV scale for HSV: H=0-179, S=0-255, V=0-255
        cv.createTrackbar('H_min', self.window_capture_trackbar , 0, 179, nothing)
        cv.createTrackbar('S_min', self.window_capture_trackbar , 0, 255, nothing)
        cv.createTrackbar('V_min', self.window_capture_trackbar , 0, 255, nothing)

        cv.createTrackbar('H_max', self.window_capture_trackbar , 0, 179, nothing)
        cv.createTrackbar('S_max', self.window_capture_trackbar , 0, 255, nothing)
        cv.createTrackbar('V_max', self.window_capture_trackbar , 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('H_max', self.window_capture_trackbar, 179)
        cv.setTrackbarPos('S_max', self.window_capture_trackbar, 255)
        cv.setTrackbarPos('V_max', self.window_capture_trackbar, 255)
        # Trackbar for increasing and decreasing saturation and value
        cv.createTrackbar('Sat_add', self.window_capture_trackbar , 0, 255, nothing)
        cv.createTrackbar('Sat_sub', self.window_capture_trackbar , 0, 255, nothing)
        cv.createTrackbar('Bright_add', self.window_capture_trackbar , 0, 255, nothing)
        cv.createTrackbar('Bright_sub', self.window_capture_trackbar , 0, 255, nothing)

    # Return an HSV filter object based on the control values
    def get_HSV_filter(self):
        hsvFilter = HSV_filter()
        hsvFilter.H_min = cv.getTrackbarPos('H_min', self.window_capture_trackbar)
        hsvFilter.S_min = cv.getTrackbarPos('S_min', self.window_capture_trackbar)
        hsvFilter.V_min = cv.getTrackbarPos('V_min', self.window_capture_trackbar)
        hsvFilter.H_max = cv.getTrackbarPos('H_max', self.window_capture_trackbar)
        hsvFilter.S_max = cv.getTrackbarPos('S_max', self.window_capture_trackbar)
        hsvFilter.V_max = cv.getTrackbarPos('V_max', self.window_capture_trackbar)
        hsvFilter.Sat_add = cv.getTrackbarPos('Sat_add', self.window_capture_trackbar)
        hsvFilter.Sat_sub = cv.getTrackbarPos('Sat_sub', self.window_capture_trackbar)
        hsvFilter.Bright_add = cv.getTrackbarPos('Bright_add', self.window_capture_trackbar)
        hsvFilter.Bright_sub = cv.getTrackbarPos('Bright_sub', self.window_capture_trackbar)
        return hsvFilter
    
    # Send image through filter and apply the filter values 
    def apply_HSV_filter(self, og_img, hsvFilter=None):
        hsv = cv.cvtColor(og_img, cv.COLOR_BGR2HSV)         # Convert image color from BGR to HSV
        if not hsvFilter:               # If no defined filter then use filter value from GUI
            hsvFilter = self.get_HSV_filter()

        # Add/subtract saturation and value 
        h, s, v = cv.split(hsv)         # Split HSV value
        s = self.shift_pixel_value(s, hsvFilter.Sat_add)
        s = self.shift_pixel_value(s, -hsvFilter.Sat_sub)
        v = self.shift_pixel_value(v, hsvFilter.Bright_add)
        v = self.shift_pixel_value(v, -hsvFilter.Bright_sub)
        hsv = cv.merge([h, s, v])       # Merge the split values back to a HSV image

        # Set min max HSV value to display
        lower = np.array([hsvFilter.H_min, hsvFilter.S_min, hsvFilter.V_min])
        upper = np.array([hsvFilter.H_max, hsvFilter.S_max, hsvFilter.V_max])
        # Apply threshold
        mask = cv.inRange(hsv, lower, upper)    # Check to see if array element lies inbetween the two other arrays
        result = cv.bitwise_and(hsv, hsv, mask=mask)    # Returns black or white image based on if pixels are lower or higher than the threshold
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)
        return img

    # Shift HSV pixel values in python using Numpy
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    def shift_pixel_value(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c
