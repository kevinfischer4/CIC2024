import cv2

def getStreamFrame(show_frame=False):
    cap = cv2.VideoCapture(0)

    # Fehlerprüfung, falls keine Kamera gefunden wird
    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden.")
        exit()
    
    # Lese ein Bild aus dem Kamerastream
    ret, frame = cap.read()
    if not ret:
        print("Fehler beim Abrufen des Bildes.")

    # Kamera und Fenster freigeben und schließen
    cap.release()
    cv2.destroyAllWindows()

    return frame
