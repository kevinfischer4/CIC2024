from findRectangels import findSortedRectangles
import json

def analyze(image):
    sorted_levers =  findSortedRectangles(image)
    lever_dimensions = json.load(open('lever_dimensions.json'))
    for i, lever in enumerate(sorted_levers):
        # Prüfen, ob max(w,h) > als lever_dimensions[i]{'closed} ist
        if max(lever[2], lever[3]) > lever_dimensions["Lever" + str(i)]['close'] * 1.05:
            print(f"Hebel {i} ist offen.")
        else:
            print(f"Hebel {i} ist geschlossen.")