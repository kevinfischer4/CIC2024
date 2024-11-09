from calibration import calibrate


START_IMAGE_NUMBER = 13
REFERENCE_IMAGE_NUMBER = 12

# calibrate the closed position
image_path_closed = 'IMG/12'
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
