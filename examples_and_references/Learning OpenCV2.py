import cv2 as cv
import numpy as np

# Read an image from file, the zero arguement makes it grayscale
image = cv.imread('C:/Users/speed/Desktop/VS Code Stuff/Uni VS Code Stuff/Github Repositories/EXPO AI Learning/Learning_AI/Images for recognition/Inside of a pipe 3.jpg', 0)

# turns the image into black and white
ret,thresh_binary = cv.threshold(image,127,255,cv.THRESH_BINARY)

# # Convert the image to grayscale
# gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# Display the image in a window
cv.imshow('Image', thresh_binary)

# Apply Gaussian blur to reduce noise
# image_blurred = cv.GaussianBlur(thresh_binary, (9, 9), 1)

# Use the Hough Circle Transform to detect circles in the image
circles = cv.HoughCircles(thresh_binary, cv.HOUGH_GRADIENT, dp=1, minDist=400, param1=50, param2=60, minRadius=0, maxRadius=500)

# Ensure that at least one circle was found
if circles is not None:
    print("Black Circle Found")
    circles = np.uint16(np.around(circles))

    for circle in circles[0, :]:
        # Extract the center and radius of the circle
        center_x, center_y, radius = circle[0], circle[1], circle[2]

        # Draw the circle on the original image
        cv.circle(thresh_binary, (center_x, center_y), radius, (170, 255, 170), 10)

    # Display the image with detected circles
    cv.imshow('Image with Circles', thresh_binary)
else:
    print("No circles found")

# Wait for a key press and close the window
cv.waitKey(0)
cv.destroyAllWindows()
# Open the default camera (camera index 0)
# cap = cv.VideoCapture(0)

# # infinite loop that keeps the camera open
# while True:
#     # Capture a frame from the camera
#     # ret is as a boolean value that represents if the frame capture was sucessful
#     ret, frame = cap.read()

#     # Display the frame
#     cv.imshow('Video', frame)

#     # Exit the loop if the 'q' key is pressed (closes the camera when q is clicked)
#     if cv.waitKey(1) == ord('q'):
#         break

# # Release the camera and close all OpenCV windows
# cap.release()
# cv.destroyAllWindows()


