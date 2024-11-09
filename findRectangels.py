import cv2
import numpy as np
from getImage import getCvImage

def findSortedRectangles(image, show_image=False):

    # Load the image
    #image = getCvImage(image_path_closed, i)

    # Convert the image to HSV color space for color detection
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define parameters for red color detection in HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv_image, lower_red, upper_red)

    # Range for upper red
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv_image, lower_red, upper_red)

    # Combine both masks
    mask = mask1 + mask2

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on size and store bounding boxes
    levers = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h > 1500:  # Filter out very small contours
            levers.append((x, y, w, h))


    # get width and height of the image
    height, width, _ = image.shape

    # draw a point at the center of the image
    cv2.circle(image, (width // 2, height // 2), 5, (0, 0, 255), -1)

    # sort the levers based on the angle between the center of the image and the center of the bounding box starting from the top right
    return sorted(levers, key=lambda lever: np.arctan2(lever[1] - height // 2, lever[0] - width // 2))

        
