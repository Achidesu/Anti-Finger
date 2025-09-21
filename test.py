from time import sleep

from PIL import Image, ImageTk # Import Pillow for image handling
import customtkinter as ctk
import tkinter as tk
import time
import threading

class AntiTriggerFingersApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI-Powered Anti-trigger Fingers")
        self.geometry("1280x800+0+0")
        self.resizable(False, False) # Prevent resizing for fixed layout
        self.configure(fg_color="#FFFFFF")

        # event
        self.key_held = False
        self.time_max = 5
        self.time_current = 0
        self.hand_posit = 0
        self.still_hold = False
        self.current_pose = 1
        self.key = ""
        self.is_pass = False
        self.round = 0
        self.set = 0
        self.pose_name = ["placeholder",
                          "เหยียดมือตรง",
                          "ทำมือคล้ายตะขอ",
                          "กำมือ",
                          "กำมือแบบเหยียดปลายนิ้ว",
                          "งอโคนนิ้วแต่เหยียดปลายนิ้วมือ"]
        self.extent = 0
        self.progress = 0

        self.time_current = self.time_max

        # keybind
        self.bind("<Key-1>", self.on_key_press)
        # self.bind("<KeyRelease-1>", self.on_key_release)

        self.bind("<Key-2>", self.on_key_press)
#         self.bind("<KeyRelease-2>", self.on_key_release)

        self.bind("<Key-3>", self.on_key_press)
#         self.bind("<KeyRelease-3>", self.on_key_release)

        self.bind("<Key-4>", self.on_key_press)
#         self.bind("<KeyRelease-4>", self.on_key_release)

        self.bind("<Key-5>", self.on_key_press)
#         self.bind("<KeyRelease-5>", self.on_key_release)

        # --- Colors ---
        self.purple_bg = "#6a0dad" # A rich purple for the header
        self.light_gray_bg = "#d9d9d9"  # Light green for the text boxes
        self.light_gray_bg_program = "white" # For the general background or other elements
        self.red_btn = "#ff5656" # Tomato color for the Reset button
        self.hover_red_bt = "#cc4444"
        self.white_fg = "#ffffff"
        self.black_fg = "black"

        # --- Fonts ---
        self.font_large_title = ("Sarabun", 30, "bold")
        self.font_medium_text = ("Sarabun", 25)
        self.font_timer = ("Sarabun", 50, "bold") # Larger for the timer
        self.font_pose_text = ("Sarabun", 28, "bold")






if __name__ == "__main__":

    app = AntiTriggerFingersApp()
    thread_2 = threading.Thread(target=app.mainloop())
    thread_2.start()
    thread_1 = threading.Thread(target=app.check_key())
    thread_1.start()