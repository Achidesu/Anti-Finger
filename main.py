import tkinter as tk
from PIL import Image, ImageTk
import os

# Create the main window
root = tk.Tk()


# --- Debugging function ---
def print_debug(text):
    """Prints debug messages to the console."""
    print(f"[Debug] : {text}")

# --- Image resizing utility ---
def resize_with_aspect_ratio(image, max_width, max_height):
    """
    Resizes an image while maintaining its aspect ratio.
    The image will fit within the given max_width and max_height.
    """
    imagename = image.filename if hasattr(image, 'filename') else "unknown"
    original_width, original_height = image.size
    ratio = min(max_width / original_width, max_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    print_debug(f"Resized image: {os.path.basename(imagename)} from {original_width}x{original_height} to {new_width}x{new_height}")
    return resized_image

# --- Define image paths ---
logo_path = "pictures/logo.png"
pose_1_path = "pictures/EX_POSE/pose1.png"
hand_sample_path = "pictures/hand_sample.png"

# --- File existence check ---
def check_file_exists(path):
    """
    Checks if a file exists at the given path.
    If not, it prints an error and exits the application.
    """
    file_name = os.path.basename(path)
    if os.path.exists(path):
        print_debug(f"File '{file_name}' exists at '{os.path.abspath(path)}'")
        return True
    else:
        print_debug(f"Error: File '{file_name}' does not exist at '{os.path.abspath(path)}'. Please ensure 'pictures' folder is present and contains required images.")
        root.destroy()
        exit()

def __init__(self):
    self.second_max = 5
    self.timer_left = 0

def timer_f(self):
    self.timer_left = self.second_max




def reset_timer():
    print_debug(f"Timer reset")

check_file_exists(logo_path)
check_file_exists(pose_1_path)
check_file_exists(hand_sample_path)

# --- Load and resize images ---
logo_image_pil = Image.open(logo_path)
logo_resized_pil = resize_with_aspect_ratio(logo_image_pil, 150, 150)
logo_tk = ImageTk.PhotoImage(logo_resized_pil)

pose_1_image_pil = Image.open(pose_1_path)
pose_1_resized_pil = resize_with_aspect_ratio(pose_1_image_pil, 600, 600)
pose_1_tk = ImageTk.PhotoImage(pose_1_resized_pil)

hand_sample_image_pil = Image.open(hand_sample_path)
hand_sample_resized_pil = resize_with_aspect_ratio(hand_sample_image_pil, 300, 300)
hand_sample_tk = ImageTk.PhotoImage(hand_sample_resized_pil)

# --- Main Window Configuration ---
root.title("AI-powered anti-trigger finger")
root.geometry("1280x800+0+0")
root.configure(bg="#F0F0F0")

# --- Top Frame (Logo and Title) ---
top_frame_root = tk.Frame(root, bg="#6A0DAD")
top_frame_root.pack(fill="x", pady=10)

Title_Logo = tk.Label(top_frame_root, image=logo_tk, bg="#6A0DAD")
Title_Logo.pack(side="left", padx=10, pady=5)

Title_Label = tk.Label(top_frame_root, text="AI-powered anti-trigger finger", font=("Arial", 24), bg="#6A0DAD", fg="white", padx=15, pady=20)
Title_Label.pack(side="left", padx=20)

# --- Left Frame (Main Pose Image) ---
left_frame = tk.Frame(root, bg="#F0F0F0")
left_frame.pack(side="left", pady=50, fill="both", expand=True)

pose_1_image_label = tk.Label(left_frame, image=pose_1_tk, bg="#F0F0F0")
pose_1_image_label.pack(expand=True, padx=50)

# --- Right Frame (Controls and Hand Sample) ---
right_frame_main = tk.Frame(root, bd=2, relief="solid", bg="#F0F0F0")
right_frame_main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# --- Top Row Container for Set and Timer ---
top_row_container = tk.Frame(right_frame_main, bg="#F0F0F0")
top_row_container.pack(side="top", fill="x", pady=(0, 30))

# --- "Set" Display Frame ---

set_times_frame = tk.Frame(top_row_container, bg="#c5e0b5", bd=1, relief="solid")
set_times_frame.pack(side="left", padx=30, pady=10, fill="both", expand=True)

Label_times_times_frame = tk.Frame(set_times_frame)
Label_times_times_frame.pack(side="top", fill="x", padx=10, pady=10)

# Label_times = tk.Label(Label_times_times_frame, text="ครั้ง : ", font=("Arial", 25), fg="black", bg="#c5e0b5")
# Label_times.pack(padx=10, pady=10)
#
# Label_set_times_number = tk.Label(Label_times_times_frame, text=1, font=("Arial", 25), fg="black", bg="#c5e0b5")
# Label_set_times_number.pack(padx=10)

# Label_set_times = tk.Label(set_times_frame, text="เซท :", font=("Arial", 30), fg="black", bg="#c5e0b5")
# Label_set_times.pack(padx=50, pady=(30, 5))
#
# Label_set_times_number = tk.Label(set_times_frame, text=1, font=("Arial", 20), fg="black", bg="#c5e0b5")
# Label_set_times_number.pack(padx=50, pady=(5, 30))

# --- Timer Display Frame ---
timer_frame = tk.Frame(top_row_container, bg="#ADD8E6", bd=1, relief="solid")
timer_frame.pack(side="right", padx=30, pady=10, fill="both", expand=True)


# Use timer_display_var with Label_timer_display
Label_timer_display = tk.Label(timer_frame, text="5S",font=("Arial", 50), fg="black", bg="#ADD8E6")
Label_timer_display.pack(padx=50, pady=(70))

# --- Bottom Row Container for Hand Sample and Controls ---
bottom_row_container = tk.Frame(right_frame_main, bg="#F0F0F0")
bottom_row_container.pack(fill="both", expand=True)

# Frame for the hand sample image, packed to the right of bottom_row_container
right_image_frame = tk.Frame(bottom_row_container, bg="#F0F0F0")
right_image_frame.pack(side="right", fill="y", padx=30, pady=20)

hand_sample_image_label = tk.Label(right_image_frame, image=hand_sample_tk, bg="#F0F0F0")
hand_sample_image_label.pack(side="right", fill="x")

# Frame to hold the labels and the reset button, packed to the left of bottom_row_container
left_controls_container = tk.Frame(bottom_row_container, bg="#F0F0F0")
left_controls_container.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Labels
label_left = tk.Label(left_controls_container, text="ท่าที่ 1", font=("Arial", 20), bg="#F0F0F0")
label_left.pack(pady=(50, 5), padx=50)

second_label_left = tk.Label(left_controls_container, text="กำมือ", font=("Arial", 20), bg="#F0F0F0")
second_label_left.pack(pady=5, padx=50)

# --- Timer control buttons ---
# Added Start and Stop buttons for demonstration.
# The "Reset" button is already defined and linked to reset_timer().

reset_button = tk.Button(left_controls_container, text="Reset", font=("Arial", 15), bg="red", fg="white", relief="raised", command=reset_timer)
reset_button.pack(pady=(5, 50), padx=20)


# Start the Tkinter event loop
root.mainloop()