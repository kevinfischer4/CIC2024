import cv2
import numpy as np
from matplotlib import pyplot as plt

# Laden des Bildes
image_path = './IMG/1.jpg'
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
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 10 and h > 10:  # Filter für Rechtecksgröße
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Bild anzeigen
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
