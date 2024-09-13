import tkinter as tk
from get_frame_data import getting_frame_data
from tkinter import filedialog
from easyocr_read_numbers import easyocr_recognition
from inspect import signature

vid_directory = "./vid_directory/"
tmplt_directory = "./tmplt_directory/"
frame_image_folder = './dmg_frame_data/'
output_csv_folder = './'

root = tk.Tk()
root.title("Frame Data Extraction")
root.geometry("600x400")

class choose_file_or_folder:
    button_label_var = tk.StringVar()

    def __init__(self, file_type, default_directory):
        self.file_type = file_type
        self.default_directory = default_directory
    def choose_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Select a file",(self.file_type))])
        if filename:
            self.default_directory = filename
            print(self.default_directory)           
            self.button_label_var.set(f"Path: {self.default_directory}")
    

def choose_vid_file():
    filename = filedialog.askopenfilename(filetypes=[("mp4 or mkv",("*.mp4","*.mkv"))])
    if filename:
        global vid_directory
        vid_directory = filename
        print(vid_directory) 
        vid_button_label_var.set(f"Vid path: {vid_directory}")
        
def choose_tmplt_file():  
    filename = filedialog.askopenfilename(filetypes=[("jpg or png",("*.jpg","*.png"))])
    if filename:
        global tmplt_directory
        tmplt_directory = filename
        print(tmplt_directory) 
        tmplt_button_label_var.set(f"Tmplt path: {tmplt_directory}")

def choose_frame_data_folder():  
    filename = filedialog.askdirectory(title="Select directory for frame data", mustexist=True)
    if filename:
        global frame_image_folder
        frame_image_folder = filename
        print(frame_image_folder) 
        frame_data_button_label_var.set(f"Data frame path: {frame_image_folder}")

def num_SmallerZero_check():
    try:
        int(interval_var.get())
        int(begin_time_var.get())
        if int(interval_var.get()) < 0 or int(begin_time_var.get()) < 0:
            raise ValueError('Negative values not allowed!')
        extract_frame_data()
    except ValueError:
        tk.messagebox.showinfo("Value error!", "Interval and Begin time must be an integer >= 0")
        return
    
def extract_frame_data():
    getting_frame_data(vid_directory, tmplt_directory, frame_image_folder, interval = int(interval_var.get()), begin_time = int(begin_time_var.get()))
    tk.messagebox.showinfo("Done","Frame data extracted successfully!")

def choose_output_csv_folder():  
    filename = filedialog.askdirectory(title="Select directory for csv file", mustexist=True)
    if filename:
        global output_csv_folder
        output_csv_folder = filename
        print(output_csv_folder) 
        csv_button_label_var.set(f"CSV path: {output_csv_folder}")

def extract_csv_data():
    easyocr_recognition(frame_image_folder, output_csv_folder)
    tk.messagebox.showinfo("Done","Output.csv created successfully!")

init_label = tk.Label(root, text="Select an option:").grid(row=0, column=1)

vid_button = tk.Button(root, text="Choose vid file", command=choose_vid_file).grid(row=1, column=1)
vid_button_label_var = tk.StringVar()
vid_button_label = tk.Label(root, textvariable=vid_button_label_var).grid(row=2, column=1)


'''
get_vid_file = choose_file_or_folder(["*.mp4","*.mkv"],vid_directory)
vid_button = tk.Button(root, text="Choose vid file", command=get_vid_file.choose_file).grid(row=1, column=1)
vid_button_label_var = get_vid_file.button_label_var
vid_button_label_var = tk.StringVar()
vid_button_label = tk.Label(root, textvariable=vid_button_label_var).grid(row=2, column=1)
'''

tmplt_button = tk.Button(root, text="Choose tmplt file", command=choose_tmplt_file).grid(row=3, column=1)
tmplt_button_label_var = tk.StringVar()
tmplt_button_label = tk.Label(root, textvariable=tmplt_button_label_var).grid(row=4, column=1)



frame_data_button = tk.Button(root, text="Choose frame data folder", command=choose_frame_data_folder).grid(row=5, column=1)
frame_data_button_label_var = tk.StringVar()
frame_data_button_label = tk.Label(root, textvariable=frame_data_button_label_var).grid(row=6, column=1)
interval_var = tk.StringVar(root, value='300')
interval_label = tk.Label(root, text=f"Capture interval in ms (default: {signature(getting_frame_data).parameters['interval'].default})").grid(row=7,column=1)
interval_entry = tk.Entry(root, textvariable=interval_var).grid(row=8,column=1)
begin_time_var = tk.StringVar(root, value='0')
begin_time_label = tk.Label(root, text=f"Begin time in ms (default: {signature(getting_frame_data).parameters['begin_time'].default})").grid(row=9,column=1)
begin_time_entry = tk.Entry(root, textvariable=begin_time_var).grid(row=10,column=1)

get_frame_button = tk.Button(root, text="Get frame data", command=num_SmallerZero_check, fg='red', pady= 5).grid(row=11, column=1, pady=10)



csv_button = tk.Button(root, text="Choose output.csv folder", command=choose_output_csv_folder).grid(row=13, column=1)
csv_button_label_var = tk.StringVar()
csv_button_label = tk.Label(root, textvariable=csv_button_label_var).grid(row=14, column=1)



get_frame_button = tk.Button(root, text="Get output.csv file", command=extract_csv_data, fg='red', pady= 5).grid(row=15, column=1, pady=10)

root.mainloop()