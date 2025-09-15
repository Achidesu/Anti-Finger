from PIL import Image, ImageTk # Import Pillow for image handling
import customtkinter as ctk
import tkinter as tk
import time

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
        self.current_pose = 1
        self.key = ""
        self.is_pass = False
        self.round = 0

        self.time_current = self.time_max

        #keybind
        self.bind("<Key-1>", self.on_key_press)
        self.bind("<KeyRelease-1>", self.on_key_release)

        self.bind("<Key-2>", self.on_key_press)
        self.bind("<KeyRelease-2>", self.on_key_release)

        self.bind("<Key-3>", self.on_key_press)
        self.bind("<KeyRelease-3>", self.on_key_release)

        self.bind("<Key-4>", self.on_key_press)
        self.bind("<KeyRelease-4>", self.on_key_release)

        self.bind("<Key-5>", self.on_key_press)
        self.bind("<KeyRelease-5>", self.on_key_release)



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
        print("[Debug] : Timer reset!")
        print("[Debug] : Hand position is rested")

    def update_pic(self):
        if self.key == "1" and self.current_pose == 1:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_1/1.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self, image=self.robot_hand_photo, text="")
            self.robot_hand_label.pack()
            self.hand_posit = 5
        elif self.key == "2" and self.current_pose == 2:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_2/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self, image=self.robot_hand_photo, text="")
            self.robot_hand_label.pack()
        elif self.key == "3" and self.current_pose == 3:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_3/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self, image=self.robot_hand_photo, text="")
            self.robot_hand_label.pack()
        elif self.key == "4" and self.current_pose == 4:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_4/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self, image=self.robot_hand_photo, text="")
            self.robot_hand_label.pack()
        elif self.key == "5" and self.current_pose == 5:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_5/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self, image=self.robot_hand_photo, text="")
            self.robot_hand_label.pack()
        else:
            print("[Debug] : Out of bounds!.")

    def reset_pic(self):
        self.robot_hand_label.destroy()
        robot_hand_image_pil = Image.open(f"pictures/pose_1/1.jpg")  # Assuming 'robot_hand.png'
        robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
        self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
        self.robot_hand_label = ctk.CTkLabel(self, image=self.robot_hand_photo, text="")
        self.robot_hand_label.pack()



    def update_timer(self):
        print(f"[Debug] : Timer : {self.time_current}")
        self.timer_canvas.delete(self.timer_text)
        self.timer_text = self.timer_canvas.create_text(100, 100, text=self.time_current, font=self.font_timer,fill=self.black_fg)


    def on_key_press(self, event=None):
        self.key = event.char
        if not self.key_held:
            self.key_held = True
            self.check_key_loop()

    def on_key_release(self, event=None):
        self.key_held = False
        self.hand_posit = 0
        self.still_hold = False

    def check_key_loop(self):
        print(f"[Debug] : {self.key} is pressed")
        if self.key_held and self.still_hold == False:
            if self.current_pose == 1 and self.key == "1":
                if self.hand_posit < 5:
                    self.hand_posit = self.hand_posit + 1
                    print(f"[Debug] : hand position is {self.hand_posit}")
                    self.update_pic()

                if self.hand_posit == 5 and self.time_current >= 0 and self.still_hold == False:
                    self.time_current = self.time_current - 1
                    self.update_timer()

                if self.time_current <= -1:
                    self.update_timer()
                    self.timer_reset()
                    self.update_timer()
                    self.reset_pic()
                    self.current_pose = self.current_pose + 1
                    print(f"[Debug] : Current pose is now {self.current_pose}")
                    self.is_pass = True
                    print("[Debug] : pose 1 pass")

            elif self.current_pose == 2 and self.key == "2":
                if self.hand_posit < 5:
                    self.hand_posit = self.hand_posit + 1
                    print(f"[Debug] : hand position is {self.hand_posit}")
                    self.update_pic()

                if self.hand_posit == 5 and self.time_current >= 0 and self.still_hold == False:
                    self.time_current = self.time_current - 1
                    self.update_timer()

                if self.time_current <= -1:
                    self.timer_reset()
                    self.update_timer()
                    self.reset_pic()
                    self.current_pose = self.current_pose + 1
                    print(f"[Debug] : Current pose is now {self.current_pose}")
                    self.is_pass = True
                    print("[Debug] : pose 2 pass")

            elif self.current_pose == 3 and self.key == "3":
                if self.hand_posit < 5:
                    self.hand_posit = self.hand_posit + 1
                    print(f"[Debug] : hand position is {self.hand_posit}")
                    self.update_pic()

                if self.hand_posit == 5 and self.time_current >= 0 and self.still_hold == False:
                    self.time_current = self.time_current - 1
                    self.update_timer()

                if self.time_current <= -1:
                    self.timer_reset()
                    self.update_timer()
                    self.reset_pic()
                    self.current_pose = self.current_pose + 1
                    print(f"[Debug] : Current pose is now {self.current_pose}")
                    self.is_pass = True
                    print("[Debug] : pose 3 pass")

            elif self.current_pose == 4 and self.key == "4":
                if self.hand_posit < 5:
                    self.hand_posit = self.hand_posit + 1
                    print(f"[Debug] : hand position is {self.hand_posit}")
                    self.update_pic()

                if self.hand_posit == 5 and self.time_current >= 0 and self.still_hold == False:
                    self.time_current = self.time_current - 1
                    self.update_timer()

                if self.time_current <= -1:
                    self.timer_reset()
                    self.update_timer()
                    self.reset_pic()
                    self.current_pose = self.current_pose + 1
                    print(f"[Debug] : Current pose is now {self.current_pose}")
                    self.is_pass = True
                    print("[Debug] : pose 4 pass")

            elif self.current_pose == 5 and self.key == "5":
                if self.hand_posit < 5:
                    self.hand_posit = self.hand_posit + 1
                    print(f"[Debug] : hand position is {self.hand_posit}")
                    self.update_pic()

                if self.hand_posit == 5 and self.time_current >= 0 and self.still_hold == False:
                    self.time_current = self.time_current - 1
                    self.update_timer()

                if self.time_current <= -1:
                    self.timer_reset()
                    self.update_timer()
                    self.reset_pic()
                    self.current_pose = 1
                    self.round = self.round + 1
                    print(f"[Debug] : Current pose is now {self.current_pose}")
                    self.is_pass = True
                    print("[Debug] : pose 5 pass")
                    print(f"[Debug] : Round : {self.round}")


            else:
                print("[Debug] : User didn't follow the instructions")


            self.after(1000, self.check_key_loop)

        else:
            print(f"[Debug] : {self.key} is released.")
            self.still_hold = False


if __name__ == "__main__":
    app = AntiTriggerFingersApp()
    app.mainloop()