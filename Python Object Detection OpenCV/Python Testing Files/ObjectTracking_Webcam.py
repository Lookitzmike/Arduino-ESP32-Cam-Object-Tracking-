import cv2 as cv

capture = cv.VideoCapture(0)        # Open a camera for video capture using external cam on PC with no internal
tracker = cv.TrackerCSRT_create()   # Select Tracker
success, img = capture.read()
# Draw box on target within the window 
boundBox = cv.selectROI("Python OpenCV Object Tracking", img, False) 
tracker.init(img,boundBox)          # Press enter to initiate tracker

def drawBox(img, boundBox):         # Get img and box 
    # Convert tuple to int 
    x = int(boundBox[0])
    y = int(boundBox[1])
    width = int(boundBox[2])
    height = int(boundBox[3])
    cv.rectangle(img, (x, y), ((x+width), (y+height)), (0, 0, 255), 3, 1)    # Color, Thickness, Line type
    cv.putText(img, "Tracking", (10,40), cv.FONT_HERSHEY_SIMPLEX , .5, (0, 255, 0), 2)   

while True:
    timer = cv.getTickCount()
    success, img = capture.read()
    success, boundBox = tracker.update(img)             # Get bounding box and update current location send to tracker

    if success:
        drawBox(img, boundBox)      # Send img and box, box list value = (X,Y, Width, Height)
    else:
        cv.putText(img, "Lost Tracking", (10,40), cv.FONT_HERSHEY_SIMPLEX , .5, (0, 0, 255), 2)   

    fps = cv.getTickFrequency()/(cv.getTickCount()-timer)   # Get fps
    # Location of fps string(int(x,y)), font, scale, color(BGR), thickness(int)
    cv.putText(img, ("FPS: " + str(int(fps))), (10,20), cv.FONT_HERSHEY_SIMPLEX , .5, (247, 67, 49), 2)   
    cv.imshow("Python OpenCV Object Tracking", img)     # Title of window 

    if cv.waitKey(1) == ord('q'):                # Quit Program if q is pressed
            cv.destroyAllWindows()
            break
