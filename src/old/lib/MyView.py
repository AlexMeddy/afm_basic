#to install opencv https://pypi.org/project/opencv-python/
import cv2


while (1):
    # Load the image
    image = cv2.imread("graph.png")

    # Display the image
    cv2.imshow("Image", image)

    # Wait for the user to press a key
    cv2.waitKey(1000)

# Close all windows
cv2.destroyAllWindows()