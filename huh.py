import numpy as np
import cv2 as cv

class VisionProcessing:

    movement_direction = ''

    def detect_circles(self, circles, thresh_binary, frame):
        # Ensure that at least one circle was found
        if circles is None:
            circle_found = 0
            
        if circles is not None:
            circles = np.uint16(np.around(circles))
            circle_found = 1
                
            for circle in circles[0, :]:
                # Extract the center and radius of the circle
                center_x, center_y, radius = circle[0], circle[1], circle[2]

                # Draw the circle on the original frame
                cv.circle(thresh_binary, (center_x, center_y), radius, (0, 255, 0), 2)

                # Check the position of the detected circle and make decisions
                height, width = frame.shape[0], frame.shape[1]
                self.movement_direction = self.make_decision(center_x, width, height)

        return circle_found

    def make_decision(self, circle_center, frame_width, frame_height):
        # Define the threshold
        left_threshold = 0.4 * frame_width
        right_threshold = 0.6 * frame_width
        up_threshold = 0.6 * frame_height
        down_threshold = 0.4 * frame_height

        x_direction = ''
        y_direction = ''
        # Check where the circle(s) is found and determine the direction
        if circle_center < left_threshold:
            x_direction = 'Left'
        elif circle_center > right_threshold:
            x_direction = 'Right'
        elif circle_center > left_threshold and circle_center < right_threshold:
            x_direction = 'Straight'
        
        if circle_center > down_threshold:
            y_direction =  'Down'
        elif circle_center < up_threshold:
            y_direction = 'Up'
        elif circle_center > up_threshold and circle_center < down_threshold:
            y_direction = 'Straight'
       
        return x_direction, y_direction
    
def camera_processing():
    # Circle Detection with a video camera

    # Open the default camera (camera index 0)
    cap = cv.VideoCapture(0)
    backSub = cv.createBackgroundSubtractorMOG2()
    if not cap.isOpened():
        print("Error opening video file")

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Apply background subtraction
            fg_mask = backSub.apply(frame)

            # Find contours
            contours, hierarchy = cv.findContours(fg_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            frame_ct = cv.drawContours(frame, contours, -1, (0, 255, 0), 2)

            # apply global threshold to remove shadows
            retval, mask_thresh = cv.threshold(fg_mask, 128, 255, cv.THRESH_BINARY)

            # set the kernal
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
            # Apply erosion
            mask_eroded = cv.morphologyEx(mask_thresh, cv.MORPH_OPEN, kernel)

            # Use the Hough Circle Transform to detect circles in the frame
            circles = cv.HoughCircles(
                mask_eroded,
                cv.HOUGH_GRADIENT,
                dp=1,
                minDist=100,  # Adjust the minimum distance between circles
                param1=10, # Adjust the sensitivity
                param2=30,   # Adjust the accuracy for circle detection
                minRadius=0,
                maxRadius=100  # Adjust the maximum radius of the circles you want to detect
            )
            # Display the resulting frame
            cv.imshow('Frame_final', mask_thresh)

        # Exit the loop if the 'q' key is pressed
        if cv.waitKey(1) == ord('q'):
            break

camera_processing()
