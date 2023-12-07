import numpy as np
import cv2 as cv
import os
from DetectionFunctions import update_Circle, get_CircleBin

Circle_Text_File_path = "CircleBin.txt"



# binary value:
# 1 - there is a circle
# 0 - there is not a circle
Circle = 0


# Open the default camera (camera index 0)
cap = cv.VideoCapture(0)

ReactionCount = 0
while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # resizes the frame, inturn making the video bigger (or smaller)
    frame = cv.resize(frame, (960, 540))
    
    # if a frame isnt found break the loop
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret,thresh_binary = cv.threshold(gray,127,255,cv.THRESH_BINARY)

    # Apply Gaussian blur to reduce noise
    blurred = cv.GaussianBlur(thresh_binary, (9, 9), 2)

    # Uses the Hough Circle function to detect circles in the frame
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
    # if a circle is found
    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        # checks 10 times if a circle is there for sure
        if ReactionCount < 100:
            ReactionCount += 1
            
            # if the reactioncount reached 100 then a circle has been "found"
            if ReactionCount == 100:
                # print("Circle found for sure")
                
                # updates the binary circle value to 1
                Circle = 1
                cv.imshow('Image with Circle', thresh_binary)
            else:
                print(f"Circle found, Reaction count = {ReactionCount}", end = '\r')
         
        for circle in circles[0, :]:
            # Extract the center and radius of the circle
            center_x, center_y, radius = circle[0], circle[1], circle[2]

            # Draw the circle on the original frame
            cv.circle(thresh_binary, (center_x, center_y), radius, (170, 255, 170), 2)

    # Display the frame with detected circles
    cv.imshow('Video with Circles', thresh_binary)

    # Exit the loop if the 'q' key is pressed
    
    # waitkey returns the ordinal value of any key press on the keyboard
    # so if that key is q it will return the ordinal value of q resolving the if condition 
    if cv.waitKey(1) == ord('q'):
        break


# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()

# prints the binary variable
print(Circle)

# updates the text file housing the binary variable in order to be used in other python files
update_Circle(Circle, Circle_Text_File_path)

