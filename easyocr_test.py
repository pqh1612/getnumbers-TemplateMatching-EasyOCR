#https://github.com/computervisioneng/text-detection-python-easyocr/blob/master/main.py

import cv2
import easyocr
THRESHOLD = 0.25

# read image
image_path = './tof_damage_text_small.png'

def easyocr_recognition(image_path):
    img = cv2.imread(image_path)

    # instance text detector
    reader = easyocr.Reader(['en'], gpu=True)

    # detect text on image
    text_ = reader.readtext(img)

    # draw bbox and text
    for t_, t in enumerate(text_):
        print(t)

        bbox, text, score = t

        if score > THRESHOLD:
            cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
            cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
    
    number_from_img = text
    return number_from_img

result = easyocr_recognition(image_path)
print(result)