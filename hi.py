import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)

# Vision processing loop
while True:

# Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    equalized_frame = cv.equalizeHist(gray)


    cv.imshow('Equalized Histogram', gray)

    # Exit the loop if the 'q' key is pressed
    if cv.waitKey(1) == ord('q'):
        break