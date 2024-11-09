from findRectangels import findSortedRectangles
import json
import cv2

def analyze(image):
    sorted_levers =  findSortedRectangles(image)
    lever_dimensions = json.load(open('lever_dimensions.json'))
    all_closed = True
    for i, lever in enumerate(sorted_levers):
        # Prüfen, ob max(w,h) > als lever_dimensions[i]{'closed} ist
        if len(sorted_levers) <= 10  and max(lever[2], lever[3]) > lever_dimensions["Lever" + str(i)]['close'] * 1.05:
            # zeichne ein rotes Rechteck um den Hebel
            cv2.rectangle(image, (lever[0], lever[1]), (lever[0] + lever[2], lever[1] + lever[3]), (0, 0, 255), 2)
            all_closed = False
        else:
            # zeichne ein grünes Rechteck um den Hebel
            cv2.rectangle(image, (lever[0], lever[1]), (lever[0] + lever[2], lever[1] + lever[3]), (0, 255, 0), 2)

    return all_closed, image

