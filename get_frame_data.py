import cv2
import os
from template_match import template_matching, detection_check
from crop_n_resize import cropping_n_resizing
INTERVAL = 400

def getting_frame_data(vid_folder, tmplt_folder):
    
    for vid_filename in os.listdir(vid_folder):
        if 'vid' in vid_filename:
            if vid_filename.endswith(".mp4") or vid_filename.endswith(".mkv"):
                vid_directory = os.path.join(vid_folder, vid_filename)
            else:
                print("Please set name and extension of video to 'vid.mp4' or 'vid.mkv'")
                exit()

        if vid_filename == None:
            print("No vid.mp4 or vid.mkv found in the directory")
            exit()

    tmplt_folder = './tmplt_directory/'
    for tmplt_filename in os.listdir(tmplt_folder):
        if 'tmplt' in tmplt_filename:
            if tmplt_filename.endswith(".png") or tmplt_filename.endswith(".jpg"):
                tmplt_directory = os.path.join(tmplt_folder, tmplt_filename)
            else:
                print("Please set name and extension of template image to 'tmplt.png' or 'tmplt.jpg'")
                exit()
                
        if tmplt_filename == None:
            print("No tmplt.png or tmplt.jpg found in the directory")
            exit()

    temp_img_directory = 'temp_img_name_doesnt_matter.png'

    video_frame_count = 0
    new_y_init = [0]

    vid = cv2.VideoCapture(vid_directory)
    template_img = cv2.imread(tmplt_directory, cv2.IMREAD_GRAYSCALE)
    _, template_img = cv2.threshold(template_img, 150, 255, cv2.THRESH_BINARY)

    while True:
        #look at a frame from the video every 'interval' until video ends
        #then check if frame has an image of the template and
        #extract small picture of template and the accompanying text

        vid.set(cv2.CAP_PROP_POS_MSEC,(video_frame_count*INTERVAL))    
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


