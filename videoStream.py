import cv2
import time

# Funktion, die aufgerufen wird, um das Bild zu verarbeiten
def process_frame(frame):
    # Beispiel: Bild anzeigen
    cv2.imshow('Frame', frame)
    # Hier kannst du deine eigene Verarbeitung einfügen
    # z.B. Bilderkennung, Speicherung, etc.
    print("Bild verarbeitet")

# Kamera starten
cap = cv2.VideoCapture(0)

# Fehlerprüfung, falls keine Kamera gefunden wird
if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden.")
    exit()

# Initialisierung der Zeit
prev_time = 0
interval = 1  # Sekunden zwischen den Frames

while True:
    # Aktuelle Zeit abrufen
    current_time = time.time()

    # Lese ein Bild aus dem Kamerastream
    ret, frame = cap.read()
    if not ret:
        print("Fehler beim Abrufen des Bildes.")
        break

    # Prüfen, ob der Intervall verstrichen ist
    if current_time - prev_time >= interval:
        # Funktion mit dem Frame aufrufen
        process_frame(frame)

        # Zeit aktualisieren
        prev_time = current_time

    # Mit 'q' beenden
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera und Fenster freigeben und schließen
cap.release()
cv2.destroyAllWindows()
