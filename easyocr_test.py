import cv2
import easyocr
import os
import numpy as np
from color_lower_upper_bound import get_limits

COLOR = [80,58,214] # manually input the BGR color (in this case, red)

def easyocr_recognition(image_folder):
    # initiate text detector instance
    reader = easyocr.Reader(['en'], gpu=True)

    # iterate over image files in the folder
    for filename in os.listdir(image_folder):

        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(image_folder, filename)
            img = cv2.imread(image_path)

            ###PREPROCESS IMAGE FOR OCR
            resize_factor = 3.0
            img = cv2.resize(img, (0, 0), fx=resize_factor, fy=resize_factor)

            # apply COLOR mask to HSV_img to get only COLOR in the original img
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_COLOR, upper_COLOR = get_limits(COLOR)
            mask = cv2.inRange(hsv_img, lower_COLOR, upper_COLOR)
            img_with_only_COLOR = cv2.bitwise_and(img, img, mask=mask)
            img = img_with_only_COLOR

            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
            _, threshold_img = cv2.threshold(blur_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            kernel = np.ones((5,5),np.uint8)
            eroded_img = cv2.erode(threshold_img, kernel, iterations=1)

            cv2.imshow("Threshold Image", threshold_img)
            cv2.imshow("Eroded Image", eroded_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            #img = threshold_img
            img = eroded_img

            text_ = reader.readtext(img, allowlist ='0123456789')
            print(text_)  #keep for debugging 

            # get text result by OCR from 'text_' list and put in output.txt
            with open('output.txt', 'a') as file:
                for t in text_:
                    coordinate, text, score = t
                    file.write(text + '\n')

image_folder = './dmg_frame_data/'
easyocr_recognition(image_folder)

