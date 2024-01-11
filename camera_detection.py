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
                height, width = frame.shape
                self.movement_direction = self.make_decision(center_x, width, height)

        else:
            circle_found = 0

        return circle_found

    def make_decision(self, circle_center_x, frame_width, frame_length):
        # Adjust this threshold based on your specific scenario
        upper_half_intensity = gray[:height // 2, :].mean()
        lower_half_intensity = gray[height // 2:, :].mean()
        left_half_intensity = gray[:, :width // 2].mean()
        right_half_intensity = gray[:, width // 2:].mean()

        # Compare the intensities and determine the direction
        if right_half_intensity > left_half_intensity and lower_half_intensity > upper_half_intensity:
            return "Move left and down"
        elif right_half_intensity < left_half_intensity and lower_half_intensity > upper_half_intensity:
            return "Move right and down"
        elif right_half_intensity > left_half_intensity and lower_half_intensity < upper_half_intensity:
            return "Move left and up"
        else:
            return "Move right and up"
            
    def camera_processing(self):
        # Circle Detection with a video camera

        # Open the default camera (camera index 0)
        cap = cv.VideoCapture(0)

        # Vision processing loop
        while True:

            # Capture a frame from the camera
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to grayscale
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

            # Display the frame with detected circles
            cv.imshow('Video with Circles', thresh_binary)

            # Exit the loop if the 'q' key is pressed
            if cv.waitKey(1) == ord('q'):
                break

        print(circle_detected_binary)
    
vp = VisionProcessing()
vp.camera_processing()
print(vp.movement_direction)