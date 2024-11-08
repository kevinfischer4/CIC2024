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
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Zeichnen der erkannten Rechtecke auf dem Originalbild
    counter = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 10 and h > 10:  # Filter für Rechtecksgröße
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            area = w * h
            print('Fläche:', area)
            counter += 1
            # schreibe die Länge und Breite des Rechtecks auf das Bild
            cv2.putText(image, f'{w}x{h}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
            # schreibe die Fläche des Rechtecks auf das Bild
            cv2.putText(image, f'{area:.0f}', (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        
    print('Anzahl der Rechtecke:', counter)

    # Bild anzeigen
    if show_image:
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()


#GPT:

image_path = '/mnt/data/12_1.jpg'

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
    if w * h > 50:  # Filter out very small contours
        levers.append((x, y, w, h))

# Sort the contours in a circular clockwise pattern starting from top-right
center_x = np.mean([lever[0] + lever[2] / 2 for lever in levers])
center_y = np.mean([lever[1] + lever[3] / 2 for lever in levers])
sorted_levers = sorted(
    levers,
    key=lambda lever: np.arctan2(lever[1] + lever[3] / 2 - center_y, lever[0] + lever[2] / 2 - center_x)
)

# Prepare JSON with max dimension (either width or height) for each lever
lever_dimensions = {f"Lever{i}": max(w, h) for i, (x, y, w, h) in enumerate(sorted_levers)}
lever_dimensions
