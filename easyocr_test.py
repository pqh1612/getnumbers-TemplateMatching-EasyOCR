import cv2
import easyocr
import os

def easyocr_recognition(image_folder):
    # initiate text detector instance
    reader = easyocr.Reader(['en'], gpu=True)

    # iterate over image files in the folder
    for filename in os.listdir(image_folder):

        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(image_folder, filename)
            img = cv2.imread(image_path)

            # make img 3 times bigger for better recognition
            resize_factor = 3.0
            img = cv2.resize(img, (0,0), fx = resize_factor, fy = resize_factor)

            text_ = reader.readtext(img)
            print(text_)  #keep for debugging 

            # get text result by OCR from 'text_' list and put in output.txt
            with open('output.txt', 'a') as file:
                for t in text_:
                    coordinate, text, score = t
                    file.write(text + '\n')

image_folder = './dmg_frame_data/'
easyocr_recognition(image_folder)

