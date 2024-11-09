import cv2

def getCvImage(image_path_closed, i):
    image_path = image_path_closed + '_' + str(i) + '.jpg'

    # Load the image
    return cv2.imread(image_path)