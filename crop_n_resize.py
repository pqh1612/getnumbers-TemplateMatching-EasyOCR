import cv2

def cropping_n_resizing(image_directory):
    img = cv2.imread(image_directory, cv2.IMREAD_UNCHANGED)
    height, width = img.shape[:2]

    #take arbitrary value to crop out as much HUD as possible
    crop_gameHUD_x1 = 0.1
    crop_gameHUD_y1 = 0.1
    crop_gameHUD_x2 = 0.85
    crop_gameHUD_y2 = 0.85

    start_row, start_col = int(height * crop_gameHUD_x1), int(width * crop_gameHUD_y1)
    end_row, end_col = int(height * crop_gameHUD_x2), int(width * crop_gameHUD_y2)
    img_cropped = img[start_row:end_row, start_col:end_col]

    #resizing
    resize_factor = 1

    img_cropped_resized = cv2.resize(img_cropped, (0,0), fx = resize_factor, fy = resize_factor)
    return img_cropped_resized