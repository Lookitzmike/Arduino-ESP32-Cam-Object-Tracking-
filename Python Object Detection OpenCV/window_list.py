import win32gui

# https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
# How to get a list of opened windows, use to select specific applications to screen capture
def winEnumHandler( window_Handle, ctx):
        if win32gui.IsWindowVisible( window_Handle ):
            print (hex(window_Handle), win32gui.GetWindowText( window_Handle ))

win32gui.EnumWindows( winEnumHandler, None)
