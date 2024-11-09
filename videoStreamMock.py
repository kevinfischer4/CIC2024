import cv2
import os
import random


def getFrame(show_frame=False):
    # Fenster freigeben und schließen
    cv2.destroyAllWindows()
    # Zufälliges Bild aus dem Ordner auswählen
    random_image_file = random.choice(image_files)
    image_path = os.path.join(image_folder, random_image_file)

    # Bild lesen
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Fehler beim Lesen des Bildes {image_path}.")

    # Bild anzeigen
    if show_frame:
        cv2.imshow('Frame', frame)
    
    return frame


# Ordnerpfad für die Bilder
image_folder = 'testImages'

# Überprüfen, ob der Ordner existiert
if not os.path.isdir(image_folder):
    print(f"Ordner '{image_folder}' nicht gefunden.")
    exit()

# Liste der Bilddateien im Ordner abrufen
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Überprüfen, ob der Ordner Bilder enthält
if not image_files:
    print(f"Keine Bilddateien im Ordner '{image_folder}' gefunden.")
    exit()





