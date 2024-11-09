from calibration import calibrate
from videoStreamMock import getFrame, process_frame
from detection import analyze
import time
import keyboard
import cv2
from handDetection import detect_hand_in_image


START_IMAGE_NUMBER = 13
REFERENCE_IMAGE_NUMBER = 12

# calibrate the closed position
image_path_closed = 'IMG/12'
cali = False
if cali:
    calibrate(image_path_closed, 'close', 0)

    # calibrate the other positions
    start_image = 100
    lever_number = 0
    for i in range(1, 31):
        image_path = 'IMG/' + str((start_image + i))
        if i % 3 == 1:
            calibrate(image_path, 'stop', lever_number)
        elif i % 3 == 2:
            calibrate(image_path, 'mid', lever_number)
        else:
            calibrate(image_path, 'open', lever_number)
            lever_number += 1

# Start the detection
# Initialisierung der Zeit
prev_time = 0
interval = 1 # Sekunden zwischen den Frames
all_closed = False
no_hands = False

while True:
    # Aktuelle Zeit abrufen
    current_time = time.time()

    # Prüfen, ob der Intervall verstrichen ist
    if current_time - prev_time >= interval:
        frame = getFrame(True)

        # Hand erkennen
        frame, no_hands = detect_hand_in_image(frame)
        if no_hands:
            all_closed, image = analyze(frame)

        
        # Funktion mit dem Frame aufrufen
    

        # Bild anzeigen
        cv2.imshow('image', image)
        cv2.waitKey(1)

        # Zeit aktualisieren
        prev_time = current_time

    # Wenn Taste gedrückt wird, beenden
    if keyboard.is_pressed('space'):
        break

    



