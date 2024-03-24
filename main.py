from get_frame_data import get_frame_data
from easyocr_test import easyocr_recognition

vid_folder = './vid_directory/'
tmplt_folder = './tmplt_directory/'
image_folder = './dmg_frame_data/'

while True:
    print("---------------------------------------------")
    print("Press [1] to extract frame data from video. Press [2] to extract number from frame data")
    print("Press [0] to exit")
    flag = str(input("Enter your choice:"))

    match flag:
        case "0":
            print("")
            print("====> Exiting program, good bye\n")
            exit()
        case "1":
            print("")
            print("====> Extracting frame data from video\n")
            get_frame_data(vid_folder, tmplt_folder)
        case "2":
            print("")
            print("====> Extracting number from frame data")
            print("====> Initalizing OCR reader, this may take a while\n")
            easyocr_recognition(image_folder)
        case other:
            print("")
            print("====> Invalid input, please try again\n")

