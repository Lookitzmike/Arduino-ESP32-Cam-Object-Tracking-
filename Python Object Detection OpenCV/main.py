import cv2 as cv
import numpy as np
import os
from time import time
from window_capture import WindowCapture
from tracking import tracking
from HSV_filter import HSV_filter

previous_time = 0                                       # Use for FPS
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # Change working dir to current folder

# The smaller the resolution the higher the frame rate use OBS video capture and use windowed projection resize resolution
# Would need to edit the HSV_filter params again and get a new face needle image
window_capture_name = WindowCapture("Windowed Projector (Source) - Video Capture Device")  # Window capture OBS webcam Projector  
#window_capture_name = WindowCapture()   # Window capture only the desktop

#tracking_Needle_img = tracking('Ball.jpg')             # Needle image for tracking the red ball in the ball gif
tracking_Needle_img = tracking('MyFace.jpg')            # Needle image for tracking my face in webcam/stream (For a 480x300p resolution)

tracking_Needle_img.init_control_gui()

""" To choose custom HSV_filter values 
comment:    hsvfilter_data = HSV_filter(0, 62, 106, 110, 110, 255, 46, 16, 0, 106)
replace:    processed_img = tracking_Needle_img.apply_HSV_filter(screenshot, hsvfilter_data) 
with:       processed_img = tracking_Needle_img.apply_HSV_filter(screenshot) 
comment:    cv.imshow('Matches', output_img)

Play around with trackbar to get HSV_filter values, crop image save as the needle image, needs to be jpg or else program won't work
replace:    tracking_Needle_img = tracking('MyFace.jpg')
Replace the 'MyFace.jpg' with the name of your needle image
"""

# HSV filter value
#hsvfilter_data = HSV_filter(0, 57, 145, 26, 255, 255, 0, 0, 0, 40)         # Filter Param for red ball and gif 
hsvfilter_data = HSV_filter(0, 32, 74, 179, 107, 255, 0, 0, 0, 53)      # Filter Param for camera of my face

while True:                                         # While loop to display frames so that it is like a video    
    screenshot = window_capture_name.get_screenshot()                   # Take a screenshot using  window capture from win32 lib

    fps = 1/( time() - previous_time )              # Calculate FPS 
    previous_time = time()
    # Location of fps string(int(x,y)), font, scale, color(BGR), thickness(int)
    cv.putText(screenshot, ("FPS: " + str(int(fps))), (10,20), cv.FONT_HERSHEY_SIMPLEX , .5, (0, 0, 255), 1)   
    #cv.imshow('ScreenCapture', screenshot)          # Create window and display screenshot

    # Pre-processing image to increase frames
    #processed_img = tracking_Needle_img.apply_HSV_filter(screenshot)        # Uncomment this and comment the line below to change filter param
    processed_img = tracking_Needle_img.apply_HSV_filter(screenshot, hsvfilter_data)

    track_obj = tracking_Needle_img.find_pos(processed_img, 0.5)               # Detection
    output_img = tracking_Needle_img.draw_rectangles(screenshot, track_obj)    # Output detection box

    cv.imshow('HSV_Filter', processed_img)       # To see the image capture with the hsv filter on for comparison 
    cv.imshow('Capture', output_img)            # To show the image capture without the filter

    if cv.waitKey(1) == ord('q'):                   # Quit Program if q is pressed
            cv.destroyAllWindows()
            break
