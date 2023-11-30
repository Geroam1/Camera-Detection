
# Open the default camera (camera index 0)
cap = cv.VideoCapture(0)

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

# Release the camera and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
