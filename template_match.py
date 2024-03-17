import cv2
import numpy as np
import datetime
import os
from color_lower_upper_bound import get_limits

DAMAGE_TEXT_HEIGHT = 1
THRESHOLD = 0.8
MAX_DIST =  100
COLOR = [80,58,214] #manually get the color red in BGR

damage_text_length = 300

def find_rightmost_red_pixel(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red, upper_red = get_limits(COLOR)
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # initialize the far rightmost x-coordinate
    rightmost_x = 0

    for contour in contours:
        x, _, w, _ = cv2.boundingRect(contour)

        # update the rightmost x-coordinate if necessary
        if x + w > rightmost_x:
            rightmost_x = x + w

    return rightmost_x

def template_matching(image_in, template_img):
    if not os.path.exists('dmg_frame_data'):
        os.makedirs('dmg_frame_data')

    img_grey = cv2.cvtColor(image_in, cv2.COLOR_BGR2GRAY)
    h, w = template_img.shape

    method = cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(img_grey, template_img, method)
    
    yloc, xloc = np.where(result >= THRESHOLD)
    return yloc, xloc, h, w

def detection_check(yloc, xloc, h, w, image_in, new_y):
    failed_detection_right_after_successful_detect = False
    
    #either yloc or xloc exists means we detect something > THRESHOLD
    detection = bool(yloc != [])
    ###LOGIC WHEN DETECTED SOMETHING
    if detection == True:
        #draw rectangle and group duplicate rectangles
        rectangles = []
        for (x, y) in zip(xloc, yloc):
            #draw two separate rectangles on top of each other to ensure proper grouping
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        for iteration, (x, y, w, h) in enumerate(rectangles):
            
            rectangle_number = np.shape(rectangles)[0]
            #print(f"No. of rectangle(s) detected: {rectangle_number}")
            rect_y_loc_list = rectangles[:,1]
            print(f"{rect_y_loc_list} - newest list of y from rectangles")

            dist_new_to_old = y - new_y[iteration]
            
            if 0 <= dist_new_to_old <= MAX_DIST:
                #damage text first appears then floats down slowly and dissipate after 1 second
                #deny rectangle generation if new detection is within 'MAX_DIST' (in pixels) below
                #the old detection to prevent duplicate captures
                print("New rect too close to old rect")
                
            else:
                failed_detection_right_after_successful_detect = True
                
                cv2.rectangle(image_in, (x, y - DAMAGE_TEXT_HEIGHT), (x + w + damage_text_length, y + h + DAMAGE_TEXT_HEIGHT), (0,255,255), 2)
                
                #crop image to get only tmplt image and numbers
                cropped_image = image_in[y - DAMAGE_TEXT_HEIGHT:y + h + DAMAGE_TEXT_HEIGHT, x:x + w + damage_text_length] 
                
                #detect red number and crop away everything else including tmplt image
                cropped_image_rightmost_red_pixel = find_rightmost_red_pixel(cropped_image)
                cropped_image = image_in[y - DAMAGE_TEXT_HEIGHT:y + h + DAMAGE_TEXT_HEIGHT, x + w : x + cropped_image_rightmost_red_pixel + 10]

                currentTime = datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S.%f")[:-3]
                cv2.imwrite('./dmg_frame_data/' + f'{currentTime}' + '_dmg_instance_' + str(iteration + 1) + '.png', cropped_image)

            if len(new_y) < rectangle_number:
                new_y = np.append(new_y, 0)

            new_y[iteration] = y

            print(f"{new_y} - new_y list")
    
    ###LOGIC WHEN NO DETECTION            
    else:
        if failed_detection_right_after_successful_detect == True:
            print("Ignore")
            failed_detection_right_after_successful_detect = False
        else:
            new_y = [0]            
            failed_detection_right_after_successful_detect = False
            print("No detection")

    return new_y

