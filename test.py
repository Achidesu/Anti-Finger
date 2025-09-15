from PIL import Image, ImageTk # Import Pillow for image handling
import customtkinter as ctk
import tkinter as tk
import time

import main
from main import *

class AntiTriggerFingersApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI-Powered Anti-trigger Fingers")
        self.geometry("1280x800+0+0")
        self.resizable(False, False) # Prevent resizing for fixed layout
        self.configure(fg_color="#FFFFFF")

        self.purple_bg = "#6a0dad" # A rich purple for the header
        self.light_gray_bg = "#d9d9d9"  # Light green for the text boxes
        self.light_gray_bg_program = "white" # For the general background or other elements
        self.red_btn = "#ff5656" # Tomato color for the Reset button
        self.hover_red_bt = "#cc4444"
        self.white_fg = "#ffffff"
        self.black_fg = "black"

        self.font_timer = ("Sarabun", 50, "bold") # Larger for the timer


        #event
        self.key_held = False
        self.time_max = 5
        self.time_current = 0
        self.hand_posit = 0
        self.still_hold = False

        self.time_current = self.time_max

        #keybind
        self.bind("<Key-1>", self.on_key_press)
        self.bind("<KeyRelease-1>", self.on_key_release)



        self.timer_canvas = ctk.CTkCanvas(self, width=200, height=200,highlightthickness=0)
        self.timer_canvas.pack()

        self.timer_canvas.create_oval(10, 10, 190, 190, outline="#3CB371", width=10)  # MediumSeaGreen
        self.timer_text = self.timer_canvas.create_text(100, 100, text=self.time_current, font=self.font_timer, fill=self.black_fg)

        robot_hand_image_pil = Image.open("pictures/pose_1/1.jpg")  # Assuming 'robot_hand.png'
        robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
        self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
        self.robot_hand_label = ctk.CTkLabel(self, image=self.robot_hand_photo, text="")
        self.robot_hand_label.pack()

    def timer_reset(self):
            self.time_current = self.time_max
            self.hand_posit = 5
            print("Timer reset!")


    def on_key_press(self, event=None):
        if not self.key_held:
            self.key_held = True
            self.check_key_loop()

    def on_key_release(self, event=None):
        self.key_held = False
        self.hand_posit = 0
        self.still_hold = False

    def check_key_loop(self):
        if self.key_held:
            if self.hand_posit < 5 :
                self.hand_posit = self.hand_posit + 1
                self.robot_hand_label.destroy()
                print(self.hand_posit)
                robot_hand_image_pil = Image.open(f"pictures/pose_1/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
                robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
                self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
                self.robot_hand_label = ctk.CTkLabel(self, image=self.robot_hand_photo, text="")
                self.robot_hand_label.pack()

            if self.hand_posit == 5 and self.time_current > 0 and self.still_hold == False:
                self.time_current = self.time_current - 1
                print(self.time_current)
                print("Key 1 is hold!")
                self.timer_canvas.delete(self.timer_text)
                self.timer_text = self.timer_canvas.create_text(100, 100, text=self.time_current, font=self.font_timer,fill=self.black_fg)
            elif self.hand_posit == 5 and self.time_current <= 0:
                self.timer_reset()
                self.still_hold = True
                self.timer_canvas.delete(self.timer_text)
                self.timer_text = self.timer_canvas.create_text(100, 100, text=self.time_current,font=self.font_timer, fill=self.black_fg)
                self.robot_hand_label.destroy()
                print(self.hand_posit)


            self.after(1000, self.check_key_loop)

        else:
            print("Key 1 is released.")



if __name__ == "__main__":
    app = AntiTriggerFingersApp()
    app.mainloop()