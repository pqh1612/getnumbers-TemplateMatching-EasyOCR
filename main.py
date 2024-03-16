import cv2
import os
from template_match import template_matching, detection_check
from crop_n_resize import cropping_n_resizing
INTERVAL = 400

#vid_directory = './vid_directory/2023-11-23 18-20-35.mkv'
vid_directory = './vid_directory/otter_multi_atk.mkv'
tmplt_directory = './tmplt_directory/tof_matching_template.png'
temp_img_directory = 'temp_image.png'

video_frame_count = 0
new_y_init = [0]

vid = cv2.VideoCapture(vid_directory)
template_img = cv2.imread(tmplt_directory, cv2.IMREAD_GRAYSCALE)


while True:
    vid.set(cv2.CAP_PROP_POS_MSEC,(video_frame_count*INTERVAL))    #extract frame from video every 'interval'
    ret, frame = vid.read()

    if ret == False:
        print("Video is over")
        break
    
    cv2.imwrite(temp_img_directory, frame)     # save frame as temporary image to be processed

    img = cropping_n_resizing(temp_img_directory)
    yloc, xloc, h, w = template_matching(img, template_img)
    new_y_init = detection_check(yloc, xloc, h, w, img, new_y_init)


    video_frame_count += 1
        
os.remove(temp_img_directory)


