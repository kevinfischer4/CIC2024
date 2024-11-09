import cv2
import numpy as np
import json
from getImage import getCvImage
from findRectangels import findSortedRectangles

def calibrate(image_path_closed, position, lever_number):
    values = []

    for i in range(1,4):
        sorted_levers = findSortedRectangles(image_path_closed, i, show_image=False)

        # Create List with max dimension (either width or height) for each lever
        if position == 'close':
            for i, (x, y, w, h) in enumerate(sorted_levers):
                if values == []:
                    values = [[] for _ in range(len(sorted_levers))] 
                    values[i] = [max(w, h)]
                else:
                    values[i].append(max(w, h))
        else:
           values.append(max(sorted_levers[lever_number][2], sorted_levers[lever_number][3]))

        # DEBUGING: Save the image with the bounding boxes of the levers
        test_indices = []
        if lever_number in test_indices:
            image = getCvImage(image_path_closed, i)

            # Draw the bounding boxes of the levers on the image
            for x, y, w, h in sorted_levers:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # write the high and width of the bounding box on the image
            for i, (x, y, w, h) in enumerate(sorted_levers):
                cv2.putText(image, f'{w} x {h} L{i}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

            # save the image
            cv2.imwrite('check/test' + str(lever_number) + position + '.jpg', image)

    # Create a dictionary to store the lever dimensions
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

