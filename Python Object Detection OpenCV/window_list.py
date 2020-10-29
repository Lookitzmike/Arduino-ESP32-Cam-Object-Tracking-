import win32gui

def winEnumHandler( window_Handle, ctx):
        if win32gui.IsWindowVisible( window_Handle ):
            print (hex(window_Handle), win32gui.GetWindowText( window_Handle ))

win32gui.EnumWindows( winEnumHandler, None)
