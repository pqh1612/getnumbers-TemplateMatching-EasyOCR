import cv2
import numpy as np
import datetime
import os
DAMAGE_TEXT_LENGTH = 200
THRESHOLD = 0.8
MAX_DIST =  100

def template_matching(image_in, template_img):
    if not os.path.exists('dmg_frame_data'):
        os.makedirs('dmg_frame_data')

    img_grey = cv2.cvtColor(image_in, cv2.COLOR_BGR2GRAY)
    #template = cv2.imread(template_directory, cv2.IMREAD_GRAYSCALE)
    h, w = template_img.shape

    method = cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(img_grey, template_img, method)
    
    yloc, xloc = np.where(result >= THRESHOLD)
    return yloc, xloc, h, w

def detection_check(yloc, xloc, h, w, image_in, new_y):
    #
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
                #deny rectangle generation if new detection is within 'max_dist' (in pixels) downwards of old detection
                #to prevent duplicate captures
                print("New rect too close to old rect")
                
            else:
                failed_detection_right_after_successful_detect = True
                

                cv2.rectangle(image_in, (x, y), (x + w + DAMAGE_TEXT_LENGTH, y + h), (0,255,255), 2)
                #crop image to get only numbers
                #cropped_image = image_in[y:y+h, x:x + w + DAMAGE_TEXT_LENGTH] 
                cropped_image = image_in

                currentTime = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S.%f")[:-3]
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

