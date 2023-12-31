import numpy as np
import cv2 as cv

class VisionProcessing:
    
    movement_direction = ''

    def detect_circles(self, circles, thresh_binary, frame):
        # Ensure that at least one circle was found
        if circles is not None:
            circles = np.uint16(np.around(circles))
            circle_found = 1
                
            for circle in circles[0, :]:
                # Extract the center and radius of the circle
                center_x, center_y, radius = circle[0], circle[1], circle[2]

                # Draw the circle on the original frame
                cv.circle(thresh_binary, (center_x, center_y), radius, (0, 255, 0), 2)

                # Check the position of the detected circle and make decisions
                self.movement_direction = self.make_decision(center_x, frame.shape[1], frame.shape[0])
                print(f'  {self.movement_direction}     ', end = '\r')

        else:
            circle_found = 0

        return circle_found
    
    def make_decision(self, circle_center_x, frame_width, frame_length):
        # Adjust this threshold based on your specific scenario
        left_threshold = 0.45 * frame_width
        right_threshold = 0.55 * frame_width
        
        down_threshold = 0.45 * frame_length
        up_threshold = 0.55 * frame_length
        
        
        # Make decisions based on the position of the detected circle
        if circle_center_x < left_threshold:
            return ('Left')
        elif circle_center_x > right_threshold:
            return ('Right')
        elif circle_center_x < down_threshold:
            return ('Down')
        elif circle_center_x > up_threshold:
            return ('Up')
        else:   
            return ('Forward')
       
    def camera_processing(self):
        # Circle Detection with a video camera

        # Open the default camera (camera index 0)
        cap = cv.VideoCapture(0)

        # sets the capture to fill the screen
        cv.namedWindow('Side-by-Side Capture', cv.WINDOW_NORMAL)
        cv.setWindowProperty('Side-by-Side Capture', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        # Vision processing loop
        while True:

            # Capture a frame from the camera
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to grayscale
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            ret, thresh_binary = cv.threshold(gray, 128, 255, cv.THRESH_BINARY)

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

            # Resizes the thresholded capture for concatnating
            thresh_binary_color = cv.cvtColor(thresh_binary, cv.COLOR_GRAY2BGR)
                
            # Concatenates the colour capture and the none colour capture
            side_by_side_frame = np.hstack((frame, thresh_binary_color))

            # Display the frames (left is RGB, right is greyscale)
            cv.imshow('Side-by-Side Capture', side_by_side_frame)
            
            # Exit the loop if the 'q' key is pressed
            if cv.waitKey(1) == ord('q'):
                break

        return circle_detected_binary

vp = VisionProcessing()
print(vp.camera_processing())

print(vp.movement_direction)