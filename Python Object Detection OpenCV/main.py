import cv2 as cv
import numpy as np
import os
from time import time
from window_capture import WindowCapture

previous_time = 0                                   # Use for FPS
os.chdir(os.path.dirname(os.path.abspath(__file__)))

window_capture_name = WindowCapture("ESP32 OV2460 - Google Chrome")

while True:                                         # While loop to display frames so that it is like a video    
    screenshot = window_capture_name.get_screenshot()                   # Take a screenshot using  window capture from win32 lib
    
    fps = 1/( time() - previous_time )              # Calculate FPS 
    previous_time = time()
    # Location of fps string(int(x,y)), font, scale, color(BGR), thickness(int)
    cv.putText(screenshot, ("FPS: " + str(int(fps))), (10,20), cv.FONT_HERSHEY_SIMPLEX , .5, (0, 0, 255), 1)   
    cv.imshow('ScreenCapture', screenshot)        # Create window and display screenshot

    if cv.waitKey(1) == ord('q'):                   # Quit Program if q is pressed
            cv.destroyAllWindows()
            break

