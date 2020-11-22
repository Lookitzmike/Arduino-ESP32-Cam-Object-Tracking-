import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:
    # Properties
    width, height = 0, 0
    window_Handle = None        # Ref. properties with self
    title_pixels, border_pixels = 0, 0
    crop_x, crop_y = 0, 0
    offset_x, offset_y = 0, 0

    # Constructor
    def __init__(self, window_name=None):           # Change to none to capture entire screen instead 
        if window_name is None:
            self.window_Handle = win32gui.GetDesktopWindow()
        else:
            self.window_Handle = win32gui.FindWindow(None, window_name)     # Capture a specific window. Does not work correctly atm
            if not self.window_Handle:                                      # Exception if window not found
                raise Exception('Window not found: {}'.format(window_name))
            
        # Get window size and resize to fit
        window_rect = win32gui.GetWindowRect(self.window_Handle)
        self.width = window_rect[2] - window_rect[0]
        self.height = window_rect[3] - window_rect[1]
        
        # Cut the title border and the side borders to fit the screen and also increase frame rates with lower resolution
        border_pixels = 8        
        title_pixels = 30
        self.width = self.width - (border_pixels * 2)
        self.height = self.height - title_pixels - border_pixels
        self.crop_x = border_pixels
        self.crop_y = title_pixels
        
    def get_screenshot(self):
        # Get window image
        wDC = win32gui.GetWindowDC(self.window_Handle)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.width, self.height) , dcObj, (self.crop_x, self.crop_y), win32con.SRCCOPY)

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

    def get_screen_position(self, pos):                 # Calculate offset position on first run, don't move window when script starts or offset will be off
        return(pos[0] + self.offset_x, pos[1] + self.offset_y)  