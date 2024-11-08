import cv2
import numpy as np
from matplotlib import pyplot as plt

START_IMAGE_NUMBER = 13
REFERENCE_IMAGE_NUMBER = 12


def calibrateCamera():
    lever_number = 1 # Rechts oben, im Uhrzeigersinn
    lever_position = 0 # 0 = Anschlag, 1 = Mitte, 2 = Offen





def findRectangle(image_path, show_image=False):
    image = cv2.imread(image_path)

    # Konvertieren in den HSV-Farbraum
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definieren der Farbgrenzen für Rot
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Maske für den roten Bereich erstellen
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask = mask1 | mask2

    # Anwenden der Maske auf das Bild
    result = cv2.bitwise_and(image, image, mask=mask)

    # Konvertieren zu Graustufen und Thresholding für die Konturerkennung
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # Finden der Konturen
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Zeichnen der erkannten Rechtecke auf dem Originalbild
    counter = 0
    for contour in contours:
        if hierarchy[0][counter][3] == -1:
            x, y, w, h = cv2.boundingRect(contour)
            if w * h > 1750:  # Filter für Rechtecksgröße
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                area = w * h
                print('Fläche:', area)
                counter += 1
                # schreibe die Länge und Breite des Rechtecks auf das Bild + Einheit
                cv2.putText(image, f'{w} x {h}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                # schreibe die Fläche des Rechtecks auf das Bild + Einheit
                cv2.putText(image, f'{area}', (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

        
    print('Anzahl der Rechtecke:', counter)

    # Bild anzeigen
    if show_image:
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()



image_path = 'IMG/12_1.jpg'

def test(image_path):


    image = cv2.imread(image_path)

    # Convert the image to RGB for display purposes if needed
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    # Define parameters for red color detection in HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
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

    # Filter contours based on size and sort clockwise starting from top-right
    levers = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h > 1750:  # Filter out very small contours
            # Filter out rectangles that are inside other rectangles
            levers.append((x, y, w, h))
            print('Lever:', x, y, w, h)

    # Sort the contours in a circular clockwise pattern starting from top-right by using arctan2
    levers.sort(key=lambda x: np.arctan2(x[1], x[0]))

    # Draw the contours on the image
    for lever in levers:
        x, y, w, h = lever
        cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # schreibe die Länge und Breite des Rechtecks auf das Bild + Einheit
        cv2.putText(image_rgb, f'{w} x {h}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    # Display the image
    plt.figure(figsize=(10, 10))
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()

    for(i, lever) in enumerate(levers):
        x, y, w, h = lever
        print(f'Lever {i}: x={x}, y={y}, w={w}, h={h}')




test(image_path)

#findRectangle(image_path, show_image=True)
