# Get numbers from video w/ template matching and EasyOCR
[![image](https://img.youtube.com/vi/ETpORNAtlVY/0.jpg)](https://www.youtube.com/watch?v=ETpORNAtlVY)

## Installation
### Install pytorch
`https://pytorch.org/get-started/locally/`
### Install requirements 
Open your code editor of choice and type
`pip install -r requirements.txt`

or `pip install -r /<path to your folder here>/requirements.txt`
## Setup
- Rename your video to `vid` with the extension `.mp4` or `.mkv` and put it in `vid_directory` folder

- Rename your template image into `tmplt` with the extension `.jpg` or `.png` and put it in `tmplt_directory` folder

  <sub>_The template image is a picture of an indicator that always appear next to the number that you want to capture_<sub/>

## Instruction
Run main.py and choose what you want to do on the terminal
![image](https://github.com/pqh1612/getnumbers-TemplateMatching-EasyOCR/assets/50303971/f621e541-d311-4b98-9814-2320ef3c23fd)
  1. Press 1: capture frame images from `vid.mp4` or `vid.mkw` located inside the `vid_directory` and save the frame images in `dmg_frame_data`
  2. Press 2: start EasyOCR reader to read the numbers from the frame images in `dmg_frame_data` and export the data to file `output.csv`
   
      <sub>_If you are starting fresh with no data: press 1 first to get the frame images from the video, then press 2 to read those frame images and get their number_<sub/>
  