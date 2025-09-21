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
        self.bind("<KeyRelease-1>", self.on_key_release)

        self.bind("<Key-2>", self.on_key_press)
        self.bind("<KeyRelease-2>", self.on_key_release)

        self.bind("<Key-3>", self.on_key_press)
        self.bind("<KeyRelease-3>", self.on_key_release)

        self.bind("<Key-4>", self.on_key_press)
        self.bind("<KeyRelease-4>", self.on_key_release)

        self.bind("<Key-5>", self.on_key_press)
        self.bind("<KeyRelease-5>", self.on_key_release)

        # --- Colors ---
        self.purple_bg = "#6a0dad" # A rich purple for the header
        self.light_gray_bg = "#d9d9d9"  # Light green for the text boxes
        self.light_gray_bg_program = "white" # For the general background or other elements
        self.red_btn = "#ff5656" # Tomato color for the Reset button
        self.hover_red_bt = "#cc4444"
        self.green_btn = "#34a853"  # Tomato color for the Reset button
        self.hover_green_bt = "#247539"
        self.white_fg = "#ffffff"
        self.black_fg = "black"

        # --- Fonts ---
        self.font_large_title = ("Sarabun", 50, "bold")
        self.font_medium_text = ("Sarabun", 40)
        self.font_timer = ("Sarabun", 50, "bold") # Larger for the timer
        self.font_pose_text = ("Sarabun", 32, "bold")

        # --- Top Bar (Header) ---
        self.top_bar_frame = ctk.CTkFrame(self, fg_color=self.purple_bg, height=150)
        self.top_bar_frame.pack(side="top", fill="x")
        self.top_bar_frame.pack_propagate(False) # Prevent frame from shrinking to fit content

        # University Logo (Placeholder)
        # Assuming you have 'hatyai_logo.png' in the same directory


        try:
            logo_image_pil = Image.open("pictures/logo.png")
            logo_image_pil = logo_image_pil.resize((150, 150), Image.LANCZOS) # Resize logo
            self.logo_photo = ImageTk.PhotoImage(logo_image_pil)
            self.logo_label = ctk.CTkLabel(self.top_bar_frame, image=self.logo_photo, fg_color=self.purple_bg, text="")
            self.logo_label.pack(side="left", padx=20, pady=10)
        except FileNotFoundError:
            self.logo_label = ctk.CTkLabel(self.top_bar_frame, text="LOGO", font=("Arial", 20), bg=self.purple_bg, fg=self.white_fg)
            self.logo_label.pack(side="left", padx=20, pady=10)
            print("Warning: hatyai_logo.png not found. Using text placeholder.")


        # App Title
        self.app_title_label = ctk.CTkLabel(self.top_bar_frame,
                                        text="AI-Powered Anti-trigger Fingers",
                                        font=self.font_large_title,
                                        text_color=self.white_fg,
                                        fg_color=self.purple_bg)
        self.app_title_label.pack(side="left", padx=20, pady=10)

        # --- Main Content Area ---
        self.main_content_frame = ctk.CTkFrame(self, fg_color=self.light_gray_bg_program)
        self.main_content_frame.pack(side="top", fill="both", expand=True, pady=20) # Add some padding from top bar

        # Use grid for the main content to arrange elements
        # Configure columns for responsiveness or specific widths
        self.main_content_frame.grid_columnconfigure(0, weight=1, minsize=400) # Left image column
        self.main_content_frame.grid_columnconfigure(1, weight=1, minsize=350) # Middle text boxes/button
        self.main_content_frame.grid_columnconfigure(2, weight=1, minsize=300) # Right timer/image column
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(1, weight=1)
        self.main_content_frame.grid_rowconfigure(2, weight=1) # For the Reset button if it was centered under text

        # --- Robot Hand Image (Left Column) ---
        try:
            robot_hand_image_pil = Image.open("pictures/pose_1/1.jpg") # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS) # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.robot_hand_photo ,text="")
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew") # Spans multiple rows
        except FileNotFoundError:
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, text="Robot Hand Image\n(Placeholder)",
                                            font=self.font_medium_text, bg="gray", fg="white", width=25, height=15)
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew")
            print("Warning: robot_hand.png not found. Using text placeholder.")

        # --- Set and Times Frame (Middle Column, Top) ---
        self.set_times_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.light_gray_bg, border_width=1)
        self.set_times_frame.grid(row=0, column=1, padx=20, pady=10, sticky="ew") # Removed expand=True to control size

        # Inner frame to keep ครั้ง and number on the same line
        self.times_line_frame = ctk.CTkFrame(self.set_times_frame, fg_color=self.light_gray_bg)
        self.times_line_frame.pack(side="top", pady=(10,0)) # Padding only top

        self.Label_times_text = ctk.CTkLabel(self.times_line_frame, text="ครั้งที่ : ", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_times_text.pack(side="left", padx=(10,0))

        self.Label_set_times_number = ctk.CTkLabel(self.times_line_frame, text=f"{self.round}", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_times_number.pack(side="left", padx=(0,10))

        # Inner frame to keep เซ็ต and number on the same line
        self.sets_line_frame = ctk.CTkFrame(self.set_times_frame, fg_color=self.light_gray_bg)
        self.sets_line_frame.pack(side="top", pady=(0,10)) # Padding only bottom

        self.Label_set_text = ctk.CTkLabel(self.sets_line_frame, text="เซ็ตที่ : ", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_text.pack(side="left", padx=(10,0))

        self.Label_set_number = ctk.CTkLabel(self.sets_line_frame, text=f"{self.set}", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_number.pack(side="left", padx=(0,10))


        # --- Pose Text (Middle Column, Middle) ---
        self.pose_text_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.light_gray_bg, border_width=1)
        self.pose_text_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.Label_pose_thai_text = ctk.CTkLabel(self.pose_text_frame, text="ท่าที่ 1", font=self.font_pose_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_pose_thai_text.pack(side="top", pady=(10,0))
        self.Label_pose_action_text = ctk.CTkLabel(self.pose_text_frame, text=f"{self.pose_name[self.current_pose]}", font=self.font_pose_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_pose_action_text.pack(side="top", pady=(0,10))

        # --- Buttons Frame (Middle Column, Bottom) ---
        self.buttons_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.light_gray_bg_program)
        self.buttons_frame.grid(row=2, column=1, columnspan=2, pady=(10, 20), sticky="w")  # <-- จาก n เป็น w

        # Start/Stop Button
        self.start_stop_button = ctk.CTkButton(
            self.buttons_frame, text="Start", font=("Sarabun", 40),
            fg_color=self.green_btn, text_color=self.white_fg,
            command=self.toggle_start_pause,
            height=35, width=150, hover_color=self.hover_green_bt)
        self.start_stop_button.pack(side="left", padx=30)


        # Reset Button
        self.reset_button = ctk.CTkButton(
            self.buttons_frame, text="Reset", font=("Sarabun", 40),
            fg_color=self.red_btn, text_color=self.white_fg,
            command=self.reset_action,height=35, width=150, hover_color=self.hover_red_bt)
        self.reset_button.pack(side="left", padx=10)




        # --- Timer Display (Right Column, Top) ---
        self.timer_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.white_fg)
        self.timer_frame.grid(row=0, column=2, padx=20, pady=20, sticky="n") # Sticky "n" to align to top

        # Create a canvas to draw the circle
        self.timer_canvas = ctk.CTkCanvas(self.timer_frame, width=200, height=200, bg=self.white_fg, highlightthickness=0)
        self.timer_canvas.pack()

        # Draw the circle (x1, y1, x2, y2)
        self.timer_canvas.create_oval(10, 10, 190, 190, outline="#3CB371", width=10,tags="progress") # MediumSeaGreen
        self.timer_text = self.timer_canvas.create_text(100, 100, text=f"{self.time_current}", font=self.font_timer, fill=self.black_fg)

        # --- Small Hand Image (Right Column, Bottom) ---
        try:
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose1.png") # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200), Image.LANCZOS) # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.small_hand_photo, text="")
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0,20), sticky="n") # Align to top
        except FileNotFoundError:
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, text="Small Hand\nImage\n(Placeholder)",
                                            font=("Arial", 16), bg="lightgray", width=15, height=10)
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0,20), sticky="n")
            print("Warning: small_hand.png not found. Using text placeholder.")

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
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.robot_hand_photo, text="")
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew")
            self.hand_posit = 5
        elif self.key == "2" and self.current_pose == 2:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_2/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.robot_hand_photo, text="")
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew")
        elif self.key == "3" and self.current_pose == 3:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_3/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.robot_hand_photo, text="")
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew")
        elif self.key == "4" and self.current_pose == 4:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_4/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.robot_hand_photo, text="")
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew")
        elif self.key == "5" and self.current_pose == 5:
            self.robot_hand_label.destroy()
            robot_hand_image_pil = Image.open(f"pictures/pose_5/{self.hand_posit}.jpg")  # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.robot_hand_photo, text="")
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew")
        else:
            print("[Debug] : Out of bounds!.")

    def reset_pic(self):
        self.robot_hand_label.destroy()
        robot_hand_image_pil = Image.open(f"pictures/pose_1/1.jpg")  # Assuming 'robot_hand.png'
        robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS)  # Adjust size as needed
        self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
        self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.robot_hand_photo, text="")
        self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew")
        self.timer_canvas.delete("progress")
        self.timer_canvas.create_oval(10, 10, 190, 190, outline="#3CB371", width=10, tags="progress")

    def update_timer(self):
        if self.time_current > 0:
            self.progress = (self.time_max - self.time_current) / self.time_max
            self.extent = 360 * self.progress
            print(f"[Debug] : Timer : {self.time_current}")
            self.timer_canvas.delete(self.timer_text)
            self.timer_canvas.delete("progress")
            self.timer_text = self.timer_canvas.create_text(100, 100, text=self.time_current, font=self.font_timer,fill=self.black_fg)
            self.timer_canvas.create_arc(10, 10, 190, 190,start=90,outline="#3CB371", width=10,extent=-self.extent,style="arc",tags="progress")
        else:
            print(f"[Debug] : Timer : {self.time_current}")
            self.timer_canvas.delete(self.timer_text)
            self.timer_text = self.timer_canvas.create_text(100, 100, text=self.time_current, font=self.font_timer,
                                                            fill=self.black_fg)
            self.timer_canvas.delete("progress")
            self.timer_canvas.create_oval(10, 10, 190, 190, outline="#3CB371", width=10, tags="progress")

    def update_round(self):
        self.Label_set_times_number.destroy()
        self.Label_set_times_number = ctk.CTkLabel(self.times_line_frame, text=f"{self.round}",font=self.font_medium_text, text_color=self.black_fg,fg_color=self.light_gray_bg)
        self.Label_set_times_number.pack(side="left", padx=(0, 10))
        self.Label_set_number.destroy()
        self.Label_set_number = ctk.CTkLabel(self.sets_line_frame, text=f"{self.set}", font=self.font_medium_text,
                                             text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_number.pack(side="left", padx=(0, 10))

    def update_EX_pose(self):
        if self.current_pose == 1:
            self.small_hand_label.destroy()
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose1.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200), Image.LANCZOS)  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.small_hand_photo, text="")
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="n")  # Align to top
        elif self.current_pose == 2:
            self.small_hand_label.destroy()
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose2.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200), Image.LANCZOS)  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.small_hand_photo, text="")
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="n")  # Align to top
        elif self.current_pose == 3:
            self.small_hand_label.destroy()
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose3.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200), Image.LANCZOS)  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.small_hand_photo, text="")
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="n")  # Align to top
        elif self.current_pose == 4:
            self.small_hand_label.destroy()
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose4.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200), Image.LANCZOS)  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.small_hand_photo, text="")
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="n")  # Align to top
        elif self.current_pose == 5:
            self.small_hand_label.destroy()
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose5.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200), Image.LANCZOS)  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.small_hand_photo, text="")
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="n")  # Align to top
        else:
            print("[Debug] Out of bound!")

    def update_text(self):
        self.Label_pose_thai_text.destroy()
        self.Label_pose_action_text.destroy()
        self.Label_pose_thai_text = ctk.CTkLabel(self.pose_text_frame, text=f"ท่าที่ {self.current_pose}", font=self.font_pose_text,
                                                 text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_pose_thai_text.pack(side="top", pady=(10, 0))

        self.Label_pose_action_text = ctk.CTkLabel(self.pose_text_frame, text=f"{self.pose_name[self.current_pose]}", font=self.font_pose_text,
                                                   text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_pose_action_text.pack(side="top", pady=(0, 10))


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
                    self.update_EX_pose()
                    self.update_text()
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
                    self.update_EX_pose()
                    self.update_text()
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
                    self.update_EX_pose()
                    self.update_text()
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
                    self.update_EX_pose()
                    self.update_text()
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
                    self.update_EX_pose()
                    self.update_text()
                    self.round = self.round + 1
                    self.update_round()
                    print(f"[Debug] : Current pose is now {self.current_pose}")
                    self.is_pass = True
                    print("[Debug] : pose 5 pass")
                    print(f"[Debug] : Round : {self.round}")


            else:
                print("[Debug] : User didn't follow the instructions")

            if self.round >= 10:
                self.round = 0
                self.set = self.set + 1
                self.update_round()

            self.after(1000, self.check_key_loop)

        else:
            print(f"[Debug] : {self.key} is released.")
            self.still_hold = False

    def reset_action(self):
        self.current_pose = 1
        self.round = 0
        self.set = 0
        self.timer_reset()
        self.update_timer()
        self.reset_pic()
        self.update_EX_pose()
        self.update_text()
        self.update_round()
        print("[Debug] : Reset action")




    def toggle_start_pause(self):
        if self.start_stop_button.cget("text") == "Start":
            self.start_stop_button.configure(text="Pause",fg_color=self.red_btn,hover_color=self.hover_red_bt)
        else:
            self.start_stop_button.configure(text="Start",fg_color=self.green_btn, hover_color=self.hover_green_bt)


# Create dummy image files for demonstration if they don't exist
# In a real application, replace these with your actual image paths
def create_dummy_images():
    try:
        Image.new('RGB', (80, 80), color = 'purple').save('hatyai_logo.png')
        Image.new('RGB', (400, 450), color = 'black').save('robot_hand.png')
        Image.new('RGB', (200, 200), color = 'white').save('small_hand.png')
        print("Dummy images created for demonstration.")
    except Exception as e:
        print(f"Could not create dummy images: {e}. Make sure Pillow is installed.")


if __name__ == "__main__":
    create_dummy_images() # Call this to create placeholder images if they don't exist
    app = AntiTriggerFingersApp()
    app.mainloop()