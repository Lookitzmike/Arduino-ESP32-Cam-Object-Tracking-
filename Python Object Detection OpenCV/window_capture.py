import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:
    # Properties
    width = 0 
    height = 0  
    window_Handle = None        # Ref. properties with self

    # Constructor
    def __init__(self, window_name):
        self.window_Handle = win32gui.FindWindow(None, window_name)     # Capture a specific window
        if not self.window_Handle:                                      # Exception if window not found
            raise Exception('Window not found: {}'.format(window_name))
        
        window_rect = win32gui.GetWindowRect(self.window_Handle)        # Get window size and resize to fit
        self.width = window_rect[2] - window_rect[0]
        self.height = window_rect[3] - window_rect[1]

    def get_screenshot(self):
        # Get window image
        wDC = win32gui.GetWindowDC(self.window_Handle)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.width, self.height) , dcObj, (8, 30), win32con.SRCCOPY)

        # Convery data so opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        screenshot = np.fromstring(signedIntsArray, dtype='uint8')
        screenshot.shape = (self.height, self.width, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.window_Handle, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        screenshot = screenshot[...,:3]                 # Drop alpha channel else error; This also reduces fps down to 20
        screenshot = np.ascontiguousarray(screenshot)   # Make image contiguous 

        return screenshot
