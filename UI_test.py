import tkinter as tk
from get_frame_data import getting_frame_data
from tkinter import filedialog

vid_directory = "./vid_directory/"
tmplt_directory = "./tmplt_directory/"

root = tk.Tk()
root.title("Frame Data Extraction")
root.geometry("500x500")

init_label = tk.Label(root, text="Select an option:").grid(row=0, column=1)


def choose_vid_file():
    global vid_directory
    filename = filedialog.askopenfilename(filetypes=[("mp4 or mkv",("*.mp4","*.mkv"))])
    if filename:
        vid_directory = filename
        print(vid_directory) 

def choose_tmplt_file():
    global tmplt_directory
    filename = filedialog.askopenfilename(filetypes=[("jpg or png",("*.jpg","*.png"))])
    if filename:
        tmplt_directory = filename
        print(tmplt_directory) 


vid_button = tk.Button(root, text="Choose vid file", command=choose_vid_file).grid(row=1, column=1)
vid_button_label = tk.Label(root, text="Vid path: "+vid_directory).grid(row=2, column=1)


tmplt_button = tk.Button(root, text="Choose tmplt file", command=choose_tmplt_file).grid(row=3, column=1)
tmplt_button_label = tk.Label(root, text="Tmplt path: "+tmplt_directory).grid(row=4, column=1)

def extract_frame_data():
    getting_frame_data(vid_directory, tmplt_directory)
    tk.messagebox.showinfo("Done","Frame data extracted successfully!")

get_frame_button = tk.Button(root, text="Get frame data", command=extract_frame_data).grid(row=5, column=1)



root.mainloop()