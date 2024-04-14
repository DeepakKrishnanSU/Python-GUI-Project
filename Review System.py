#Deepak Krishnan S U
#URK23CS1121
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import PIL.Image, PIL.ImageTk
import threading
import imutils

# Global variables
stream = None
set_width, set_height = 640, 480

# Function to open a video file
def open_video_from_file():
    global stream
    video_link = filedialog.askopenfilename()
    if video_link and video_link.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        stream = cv2.VideoCapture(video_link)
        if stream.isOpened():
            print("Video loaded successfully.")
        else:
            print("Error: Unable to open the video file.")
    else:
        print("Error: Invalid video file.")

# Function to play the video or jump to a specific timestamp
def play(speed=None, timestamp=None):
    global stream
    if stream is None:
        print("Error: No video loaded.")
        return
    if speed:
        frame_pos = stream.get(cv2.CAP_PROP_POS_FRAMES)
        stream.set(cv2.CAP_PROP_POS_FRAMES, frame_pos + speed)
    elif timestamp:
        frame_rate = stream.get(cv2.CAP_PROP_FPS)
        target_frame = int(timestamp * frame_rate)
        stream.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=set_width, height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

# GUI setup
window = tk.Tk()
window.configure(bg='white')
window.title("Video Player")

#Canva for video playing
canvas = tk.Canvas(window, width=set_width, height=set_height)
canvas.grid(row=0, column=0, columnspan=3)

#Button to play the video frames backwards and forwards 
frame1 = ttk.LabelFrame(window, text='Controls', style='TFrame')
btn_prev_slow = ttk.Button(frame1, text="<< Previous (slow)", width=20, command=lambda: play(-2))
btn_next_slow = ttk.Button(frame1, text="Next (slow) >>", width=20, command=lambda: play(2))
frame1.grid(row=1, column=0, padx=5, pady=5)
btn_prev_slow.grid(row=0, column=0, padx=5, pady=2)
btn_next_slow.grid(row=0, column=1, padx=5, pady=2)

#Button to jump to the provided timestamp
frame2 = ttk.LabelFrame(window, text="Jump to Timestamp", style='TFrame')
timestamp_label = ttk.Label(frame2, text="Enter timestamp (seconds):")
timestamp_entry = ttk.Entry(frame2, width=20)
btn_jump = ttk.Button(frame2, text="Jump", command=lambda: play(timestamp=float(timestamp_entry.get())))
frame2.grid(row=1, column=1, padx=5, pady=5)
timestamp_label.grid(row=0, column=0, padx=5, pady=2)
timestamp_entry.grid(row=0, column=1, padx=5, pady=2)
btn_jump.grid(row=0, column=2, padx=5, pady=2)

#Button to load a video from a file
frame3 = ttk.LabelFrame(window, text="Open Video", style='TFrame')
video_link_label = ttk.Label(frame3, text="Select a video file:")
btn_open_from_file = ttk.Button(frame3, text="Open from File", width=20, command=open_video_from_file)
frame3.grid(row=1, column=2, padx=5, pady=5)
video_link_label.grid(row=0, column=0, padx=5, pady=2)
btn_open_from_file.grid(row=1, column=0, padx=5, pady=2)

window.mainloop()