import cv2 as cv
import numpy as np
import os
from time import time
from window_capture import WindowCapture
from tracking import tracking
from HSV_filter import HSV_filter

previous_time = 0                                       # Use for FPS
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # Change working dir to current folder
window_capture_name = WindowCapture()               # Window Capture None = desktop

tracking_Needle_img = tracking('Ball.jpg')                # Needle image, change image for different tracking

tracking_Needle_img.init_control_gui()

# Ball HSV filter value
hsvfilter_data = HSV_filter(0, 57, 145, 26, 255, 255, 0, 0, 0, 40)

while True:                                         # While loop to display frames so that it is like a video    
    screenshot = window_capture_name.get_screenshot()                   # Take a screenshot using  window capture from win32 lib
    
    fps = 1/( time() - previous_time )              # Calculate FPS 
    previous_time = time()
    # Location of fps string(int(x,y)), font, scale, color(BGR), thickness(int)
    cv.putText(screenshot, ("FPS: " + str(int(fps))), (10,20), cv.FONT_HERSHEY_SIMPLEX , .5, (0, 0, 255), 1)   
    #cv.imshow('ScreenCapture', screenshot)          # Create window and display screenshot

    # Pre-processing image to increase frames
    processed_img = tracking_Needle_img.apply_HSV_filter(screenshot, hsvfilter_data)

    track_obj = tracking_Needle_img.find_pos(processed_img, 0.5)               # Detection
    output_img = tracking_Needle_img.draw_rectangles(screenshot, track_obj)    # Output detection box
    
    cv.imshow('Processed', processed_img)
    cv.imshow('Matches', output_img)

    if cv.waitKey(1) == ord('q'):                   # Quit Program if q is pressed
            cv.destroyAllWindows()
            break

