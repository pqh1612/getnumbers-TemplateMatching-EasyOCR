from get_frame_data import getting_frame_data
from easyocr_read_numbers import easyocr_recognition
import tkinter as tk
from tkinter import messagebox
from get_frame_data import getting_frame_data
from easyocr_read_numbers import easyocr_recognition

vid_folder = './vid_directory/'
tmplt_folder = './tmplt_directory/'
image_folder = './dmg_frame_data/'

def extract_frame_data():
    getting_frame_data(vid_folder, tmplt_folder)
    messagebox.showinfo("Extraction Complete", "Frame data extracted successfully!")

def extract_number():
    messagebox.showinfo("OCR Reader", "Initializing OCR reader, this may take a while...")
    easyocr_recognition(image_folder)
    messagebox.showinfo("Extraction Complete", "Number extracted successfully!")

def exit_program():
    if messagebox.askokcancel("Exit Program", "Are you sure you want to exit?"):
        root.destroy()

root = tk.Tk()
root.title("Frame Data Extraction")
root.geometry("300x200")

label = tk.Label(root, text="Select an option:")
label.pack(pady=10)

frame_data_button = tk.Button(root, text="Extract Frame Data", command=extract_frame_data)
frame_data_button.pack(pady=5)

number_button = tk.Button(root, text="Extract Number", command=extract_number)
number_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack(pady=5)

root.mainloop()
            
#print("====> Invalid input, please try again\n")

