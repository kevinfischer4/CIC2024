import mediapipe as mp
import cv2



# Haarcascade für Handerkennung (muss heruntergeladen werden, wenn noch nicht vorhanden)
hand_cascade = cv2.CascadeClassifier('hand.xml')  # Beispielpfad, falls verfügbar

def detect_hand_in_image(image):
    # Bild laden und in Graustufen umwandeln
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Handerkennung durchführen
    hands = hand_cascade.detectMultiScale(image, 1.1, 5)

    # Überprüfen, ob Hände erkannt wurden
    if len(hands) > 0:
        # Hände im Bild markieren
        for (x, y, w, h) in hands:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
        print("Hand erkannt")
        return image, False
    else:
        return image, True
