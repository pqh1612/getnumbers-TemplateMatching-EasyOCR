import cv2
import easyocr
import os
import numpy as np
import csv
from color_lower_upper_bound import get_limits

COLOR = [80,58,214] # manually input the BGR color (in this case, red)

def easyocr_recognition(image_folder, output_folder):

    # initiate text detector instance
    reader = easyocr.Reader(['en'], gpu=True)

    # iterate over image files in the folder
    for filename in os.listdir(image_folder):

        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(image_folder, filename)
            img = cv2.imread(image_path)

            img = img_preprocessing(img)

            text_ = reader.readtext(img, allowlist ='0123456789')
            print(text_)  #keep for debugging 

            # get text result by OCR from 'text_' list and put in output.csv
            with open(output_folder + '/' + '/output.csv', 'a', newline='') as csvfile:
                header = ["Text", "File name"]
                writer = csv.DictWriter(csvfile, fieldnames=header)
                if csvfile.tell() == 0:
                    writer.writeheader()
                for t in text_:
                    _, text, _ = t
                    writer.writerow({header[0]: text, header[1]: filename})
                    
def img_preprocessing(image):
    ###PREPROCESS IMAGE FOR OCR
    resize_factor = 4.0
    img = cv2.resize(image, (0, 0), fx=resize_factor, fy=resize_factor)

    # apply COLOR mask to HSV_img to get only COLOR in the original img
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_COLOR, upper_COLOR = get_limits(COLOR)
    mask = cv2.inRange(hsv_img, lower_COLOR, upper_COLOR)
    img = cv2.bitwise_and(img, img, mask=mask)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    kernel = np.ones((5,5),np.uint8)
    img = cv2.erode(img, kernel, iterations = 2)
    img = cv2.dilate(img, kernel, iterations = 1)
    
    return img
