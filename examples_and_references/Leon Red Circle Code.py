import numpy as np
import cv2 as cv

# Open the default camera (camera index 0)
stream = cv.VideoCapture(0)
if not stream.isOpened():
    print("Camera failed to open")
    exit()

# Define lower and upper HSV thresholds for detecting red color
RED_LOWTRESH = np.array([0, 145, 145])
RED_HIGHTRESH = np.array([10, 240, 240])

# Setup SimpleBlobDetector parameters.
params = cv.SimpleBlobDetector_Params()

# Change the threshold values for blob detection
params.minThreshold = 200
params.maxThreshold = 255

# Filter by area (blob size)
params.filterByArea = True
params.minArea = 1000
params.maxArea = 100000

# Filter by circularity
params.filterByCircularity = True
params.minCircularity = 0.5

# Filter by convexity (degree of convex shape)
params.filterByConvexity = False
params.minConvexity = 0.87

# Filter by inertia (elongation)
params.filterByInertia = False
params.minInertiaRatio = 0.1

# Create a blob detector with the specified parameters
detector = cv.SimpleBlobDetector_create(params)

# Start an infinite loop for video processing
while True:
    # Read a frame from the camera
    ret, frame = stream.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert the frame to the HSV color space
    HSVframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Apply a blur to reduce noise in the image
    HSVframe = cv.blur(HSVframe, (3, 3))

    # Create a mask to isolate red color based on the defined thresholds
    colorMask = cv.inRange(HSVframe, RED_LOWTRESH, RED_HIGHTRESH)

    # Invert the mask to keep the red areas white
    colorMaskInverted = cv.bitwise_not(colorMask)

    # Apply the mask to the original frame to extract red regions
    colorOutput = cv.bitwise_and(frame, frame, mask=colorMask)

    # Convert the color output to grayscale
    gray = cv.cvtColor(colorOutput, cv.COLOR_BGR2GRAY)

    # Detect blobs (red circles) in the inverted mask
    keypoints = detector.detect(colorMaskInverted)

    # Draw the detected blobs (red circles) on the original frame
    frame = cv.drawKeypoints(frame, keypoints, np.array([]), (0, 255, 0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Display the original frame with the detected circles and the color-filtered output side by side
    cv.imshow("output", np.hstack([frame, colorOutput]))

    # Exit the loop if the 'q' key is pressed
    if cv.waitKey(1) == ord('q'):
        break

# Release the camera and close all OpenCV windows
stream.release()
cv.destroyAllWindows()

# Start an infinite loop for video processing
while True:
    # Read a frame from the camera
    ret, frame = stream.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert the frame to the HSV color space
    HSVframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Apply a blur to reduce noise in the image
    HSVframe = cv.blur(HSVframe, (3, 3))

    # Create a mask to isolate red color based on the defined thresholds
    colorMask = cv.inRange(HSVframe, RED_LOWTRESH, RED_HIGHTRESH)

    # Invert the mask to keep the red areas white
    colorMaskInverted = cv.bitwise_not(colorMask)

    # Apply the mask to the original frame to extract red regions
    colorOutput = cv.bitwise_and(frame, frame, mask=colorMask)

    # Convert the color output to grayscale
    gray = cv.cvtColor(colorOutput, cv.COLOR_BGR2GRAY)

    # Detect blobs (red circles) in the inverted mask
    keypoints = detector.detect(colorMaskInverted)

    # Draw the detected blobs (red circles) on the original frame
    frame = cv.drawKeypoints(frame, keypoints, np.array([]), (0, 255, 0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Display the original frame with the detected circles and the color-filtered output side by side
    cv.imshow("output", np.hstack([frame, colorOutput]))

    # Check if any keypoints are detected (i.e., red circles)
    if len(keypoints) > 0:
        print("I found a red circle")
        break

    # Exit the loop if the 'q' key is pressed
    if cv.waitKey(1) == ord('q'):
        break

# Release the camera and close all OpenCV windows
stream.release()
cv.destroyAllWindows()
