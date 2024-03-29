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
                self.movement_direction = self.make_decision(center_x, center_y, width, height)

        return circle_found

    def make_decision(self, circle_center_x, circle_center_y, frame_width, frame_height):
        # Define the threshold
        straight_threshold = 100
        left_threshold = (frame_width / 2) - straight_threshold
        right_threshold = (frame_width / 2) + straight_threshold
        up_threshold = (frame_height / 2) - straight_threshold
        down_threshold = (frame_height / 2) + straight_threshold

        x_direction = ''
        y_direction = ''
        # Check where the circle(s) is found and determine the direction
        if circle_center_x < left_threshold:
            x_direction = 'Left'
        elif circle_center_x > right_threshold:
            x_direction = 'Right'
        elif circle_center_x > left_threshold and circle_center_x < right_threshold:
            x_direction = 'Straight'
        
        if circle_center_y > down_threshold:
            y_direction =  'Down'
        elif circle_center_y < up_threshold:
            y_direction = 'Up'
        elif circle_center_y > up_threshold and circle_center_y < down_threshold:
            y_direction = 'Straight'
       
        return x_direction, y_direction
    
    def camera_processing(self, frame):
        # Circle Detection with a video camera

        # Open the default camera (camera index 0)
        cap = cv.VideoCapture(0)

        # Vision processing loop
        while True:

            # # Capture a frame from the camera
            # ret, frame = cap.read()
            # if not ret:
            #     break

            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            ret, thresh_binary = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)

            # Apply Gaussian blur to reduce noise
            blurred = cv.GaussianBlur(thresh_binary, (9, 9), 2)

            # Use the Hough Circle Transform to detect circles in the frame
            circles = cv.HoughCircles(
                blurred,
                cv.HOUGH_GRADIENT,
                dp=1,
                minDist=100,  # Adjust the minimum distance between circles
                param1=10, # Adjust the sensitivity
                param2=30,   # Adjust the accuracy for circle detection
                minRadius=0,
                maxRadius=100  # Adjust the maximum radius of the circles you want to detect
            )

            # Return whether circle(s) is detected (1 if yes, 0 otherwise)
            circle_detected_binary = self.detect_circles(circles, thresh_binary, frame)
            print(vp.movement_direction)
            # Display the frame with detected circles
            cv.imshow('Video with Circles', thresh_binary)

            # Exit the loop if the 'q' key is pressed
            if cv.waitKey(1) == ord('q'):
                break

            output = [circle_detected_binary, self.movement_direction]

        return output