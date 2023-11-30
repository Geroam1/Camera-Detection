import numpy as np
import cv2 as cv
from detection_functions import update_Circle

# Open the default camera (camera index 0)
cap = cv.VideoCapture(0)

# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()

# Circle Detection with video camera

# Open the default camera (camera index 0)
cap = cv.VideoCapture(0)

circle_found = []

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret,thresh_binary = cv.threshold(gray,127,255,cv.THRESH_BINARY)

    # Apply Gaussian blur to reduce noise
    blurred = cv.GaussianBlur(thresh_binary, (9, 9), 2)

    # Use the Hough Circle Transform to detect circles in the frame
    circles = cv.HoughCircles(
        blurred,
        cv.HOUGH_GRADIENT,
        dp=1,
        minDist=100,  # Adjust the minimum distance between circles
        param1=50,
        param2=30,   # Adjust this threshold for circle detection
        minRadius=0,
        maxRadius=100  # Adjust the maximum radius of the circles you want to detect
    )

    # Ensure that at least one circle was found
    if circles is not None:
        circles = np.uint16(np.around(circles))
        circle_found.append(1)
         
        for circle in circles[0, :]:
            # Extract the center and radius of the circle
            center_x, center_y, radius = circle[0], circle[1], circle[2]

            # Draw the circle on the original frame
            cv.circle(thresh_binary, (center_x, center_y), radius, (0, 255, 0), 2)
    else:
        circle_found.append(0)

    # Display the frame with detected circles
    cv.imshow('Video with Circles', thresh_binary)

    # Exit the loop if the 'q' key is pressed
    if cv.waitKey(1) == ord('q'):
        break


print(circle_found)


# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()