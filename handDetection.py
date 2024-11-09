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
    
def analyzeWithMediapipe(image):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True)
    mp_draw = mp.solutions.drawing_utils

    # Laden Sie Ihr Bild
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Verarbeiten des Bildes
    result = hands.process(image_rgb)

    # Überprüfen, ob Hände erkannt wurden
    if result.multi_hand_landmarks:
        print("Hand erkannt")
        for handLms in result.multi_hand_landmarks:
            # Zeichnen der Handlandmarken auf dem Bild
            mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)
        
        return image, False
    else:
        print("Keine Hand erkannt")
        return image, True

    # Anzeigen des Bildes
    cv2.imshow("Bild mit erkannter Hand", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()