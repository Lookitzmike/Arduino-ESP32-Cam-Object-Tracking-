import cv2 as cv
import numpy as np
import os
import win32gui, win32ui, win32con
from time import time

previous_time = 0                                   # Use for FPS
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def window_capture():
    width, height = 1280, 720   # Resolution 

    # Get window image
    #window_Handle = win32gui.FindWindow(None, windowname)    # Capture a specific window for example, capture only chrome. 
    window_Handle = None
    wDC = win32gui.GetWindowDC(window_Handle)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height) , dcObj, (0, 0), win32con.SRCCOPY)
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    screenshot = np.fromstring(signedIntsArray, dtype='uint8')
    screenshot.shape = (height, width, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(window_Handle, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    screenshot = screenshot[...,:3]                 # Drop alpha channel else error; This also reduces fps down to 20
    screenshot = np.ascontiguousarray(screenshot)   # Make image contiguous 

    return screenshot

define onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print('x = %d, y = %d' %(x, y))

while True:                                         # While loop to display frames so that it is like a video    
    screenshot = window_capture()                   # Take a screenshot using  window capture from win32 lib
    
    fps = 1/( time() - previous_time )              # Calculate FPS 
    previous_time = time()
    # Location of fps string(int(x,y)), font, scale, color(BGR), thickness(int)
    cv.putText(screenshot, ("FPS: " + str(int(fps))), (10,20), cv.FONT_HERSHEY_SIMPLEX , .5, (0, 0, 255), 1)   
    cv.imshow('ScreenCapture', screenshot)        # Create window and display screenshot

    if cv.waitKey(1) == ord('q'):                   # Quit Program if q is pressed
            cv.destroyAllWindows()
            break

