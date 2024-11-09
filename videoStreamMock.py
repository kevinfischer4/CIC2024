import cv2
import time
import os
import random

# Funktion, die aufgerufen wird, um das Bild zu verarbeiten
def process_frame(frame):
    # Beispiel: Bild anzeigen
    cv2.imshow('Frame', frame)
    # Hier kannst du deine eigene Verarbeitung einfügen
    print("Bild verarbeitet")

# Ordnerpfad für die Bilder
image_folder = 'IMG'

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

# Initialisierung der Zeit
prev_time = 0
interval = 1  # Sekunden zwischen den Frames

while True:
    # Aktuelle Zeit abrufen
    current_time = time.time()

    # Prüfen, ob der Intervall verstrichen ist
    if current_time - prev_time >= interval:
        # Zufälliges Bild aus dem Ordner auswählen
        random_image_file = random.choice(image_files)
        image_path = os.path.join(image_folder, random_image_file)

        # Bild lesen
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Fehler beim Lesen des Bildes {image_path}.")
            continue

        # Funktion mit dem Frame aufrufen
        process_frame(frame)

        # Zeit aktualisieren
        prev_time = current_time

    # Mit 'q' beenden
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fenster freigeben und schließen
cv2.destroyAllWindows()
