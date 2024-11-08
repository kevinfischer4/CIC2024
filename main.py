import cv2
import numpy as np
from matplotlib import pyplot as plt
import json

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


def calibrate(image_path_closed, position, lever_number):

    values = []

    for i in range(1,4):
        image_path = image_path_closed + '_' + str(i) + '.jpg'

        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to HSV color space for color detection
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define parameters for red color detection in HSV
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

        # Filter contours based on size and store bounding boxes
        levers = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w * h > 1500:  # Filter out very small contours
                levers.append((x, y, w, h))

        # Calculate the approximate center of the bounding boxes for ordering purposes
        #center_x = np.mean([lever[0] + lever[2] / 2 for lever in levers])
        #center_y = np.mean([lever[1] + lever[3] / 2 for lever in levers])


        # get width and height of the image
        height, width, _ = image.shape

        # draw a point at the center of the image
        cv2.circle(image, (width // 2, height // 2), 5, (0, 0, 255), -1)

        # sort the levers based on the angle between the center of the image and the center of the bounding box starting from the top right
        sorted_levers = sorted(levers, key=lambda lever: np.arctan2(lever[1] - height // 2, lever[0] - width // 2))

        


        # Prepare JSON with max dimension (either width or height) for each lever
        # Format should look like: {"Lever0": {"close": 100}, "Lever1": {"close": 200}, ...}  
        if position == 'close':
            for i, (x, y, w, h) in enumerate(sorted_levers):
                if values == []:
                    values = [[] for _ in range(len(sorted_levers))] 
                    values[i] = [max(w, h)]
                else:
                    values[i].append(max(w, h))
        else:
            # Append the max of width and height for lever levernumber to the values list
           values.append(max(sorted_levers[lever_number][2], sorted_levers[lever_number][3]))



        test_indices = []

        if lever_number in test_indices:
            #print('Lever:', lever_number)
            # Draw the bounding boxes of the levers on the image
            for x, y, w, h in sorted_levers:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # write the high and width of the bounding box on the image
            for i, (x, y, w, h) in enumerate(sorted_levers):
                cv2.putText(image, f'{w} x {h} L{i}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)


            # save the image
            cv2.imwrite('check/test' + str(lever_number) + position + '.jpg', image)




    #print(values)

    lever_dimensions = {}

    # Calculate the average of the max dimensions for each lever

    if position == 'close':
        for i, lever_values in enumerate(values):
            lever_dimensions[f'Lever{i}'] = {
                'close': int(np.mean(lever_values)),
                'stop': None,
                'mid': None,
                'open': None
            }
        # Write the lever dimensions to a JSON file
        with open('lever_dimensions.json', 'w') as f:
            json.dump(lever_dimensions, f, indent=4)
    else:
        # open lever_dimensions.json file and write the mean value for the specific lever and position
        with open('lever_dimensions.json', 'r+') as f:
            lever_dimensions = json.load(f)
            lever_dimensions[f'Lever{lever_number}'][position] = int(np.mean(values))
            # delete the old content of the file
            f.seek(0)
            f.truncate()
            # write the new content to the file
            json.dump(lever_dimensions, f, indent=4)


        
    #print(lever_dimensions)




image_path_closed = 'IMG/12'
start_image = 100

calibrate(image_path_closed, 'close', 0)

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



    



#findRectangle(image_path, show_image=True)
