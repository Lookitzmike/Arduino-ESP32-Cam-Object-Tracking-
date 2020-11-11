Libraries needed: Use pip install
    >> opencv-python
    >> opencv-contrib-python
    >> pywin32
    >> pywinauto

OpenCV Trackers Available:
    KCF     - Fast Tracking can handle slow FPS
    CSRT    - More accurate than KCF but slower 
    MOSSE   - Fastest tracking but not as Accurate
    GOTURN
    MedianFlow
    TLD
    BOOSTING
    MIL
    
To Do: Webcam
    >> Reset tracker if it goes off screen
    >> Use object recognition because the bounding box tracks whatever is in front thats blocking the initial object
    >> Implement Screen capture
    >> Button to swap between webcam and screen

To Do: Screen capture
    >> 
    >> 
    >> 

Note to self:
    >> Origin = 960, 540 on a 1920 x 1080 display image
    >> Top left (x, y) = 0 || Bottom right (x = 1919, y = 1079)