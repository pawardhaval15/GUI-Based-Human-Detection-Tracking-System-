import tkinter as tk
from PIL import Image, ImageTk
import threading

gif_frames = []
frames_delay = 0

def ready_gif():
    global frames_delay
    gif_file = Image.open("Images/main-gif.gif")
    
    for r in range(0, gif_file.n_frames):
        gif_file.seek(r)
        frame = gif_file.copy()
        # Crop the frame to remove the white border
        frame = remove_white_border(frame)
        gif_frames.append(frame)
    
    frames_delay = gif_file.info['duration']
    play_gif()

def remove_white_border(frame):
    # Convert the frame to RGBA mode (necessary for transparency)
    frame = frame.convert("RGBA")
    
    # Get the alpha channel as a separate image
    alpha = frame.split()[3]
    
    # Get the bounding box of the non-white region
    bbox = alpha.getbbox()
    
    # Crop the frame using the bounding box
    if bbox:
        frame = frame.crop(bbox)
    
    return frame

frame_count = -1

def play_gif():
    global frame_count, current_frame

    if frame_count >= len(gif_frames) - 1:
        frame_count = -1
        play_gif()
    else:
        frame_count += 1
        current_frame = ImageTk.PhotoImage(gif_frames[frame_count])
        gif_lb.config(image=current_frame)
    
    window.after(frames_delay, play_gif)

window = tk.Tk()
gif_lb = tk.Label(window)
gif_lb.pack()
gif_lb.place(x=360, y=240)

threading.Thread(target=ready_gif).start()

window.mainloop()
