from PIL import Image, ImageTk      # Import Pillow for handling images
import customtkinter as ctk         # CustomTkinter for modern Tkinter UI
import threading
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008             # Library for MCP3008 ADC
import time
from datetime import datetime
from playsound import playsound

# Main Application Class
class AntiTriggerFingersApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI-Powered Anti-trigger Fingers")
        self.attributes("-fullscreen", True)
        self.geometry("1280x800+0+0")
        self.overrideredirect(True)  # Remove window border
        self.bind("<Escape>", lambda e: self.destroy()) # Press ESC to quit
        self.resizable(False, False) # Prevent resizing for fixed layout
        self.configure(fg_color="#FFFFFF")
 
        # --- State Variables ---
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
        
        # --- Initialize MCP3008 ADC ---
        SPI_PORT   = 0
        SPI_DEVICE = 0
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
        
        # --- UI Colors ---
        self.purple_bg = "#6a0dad" 
        self.light_gray_bg = "#d9d9d9"  
        self.light_gray_bg_program = "white" 
        self.red_btn = "#ff5656" 
        self.hover_red_bt = "#cc4444"
        self.yellow_btn = "#fbbc05"
        self.hover_yellow_bt = "#e0a800"
        self.green_btn = "#34a853" 
        self.hover_green_bt = "#247539"
        self.white_fg = "#ffffff"
        self.black_fg = "black"
        
        # --- Fonts ---
        self.font_large_title = ("TH Sarabun", 60, "bold")
        self.font_medium_text = ("TH Sarabun", 50 ,"bold")
        self.font_timer = ("TH Sarabun", 60, "bold")
        self.font_pose_text = ("TH Sarabun", 50, "bold")
        
        # --- Top Bar (Header) ---
        self.top_bar_frame = ctk.CTkFrame(self, fg_color=self.purple_bg, height=150)
        self.top_bar_frame.pack(side="top", fill="x")
        self.top_bar_frame.pack_propagate(False) # Prevent frame from shrinking to fit content

        # HTC Logo (Placeholder)
        # Assuming you have 'hatyai_logo.png' in the same directory
        try:
            logo_image_pil = Image.open("pictures/logo.png")
            logo_image_pil = logo_image_pil.resize((130, 130)) # Resize logo
            self.logo_photo = ImageTk.PhotoImage(logo_image_pil)
            self.logo_label = ctk.CTkLabel(self.top_bar_frame, image=self.logo_photo, fg_color=self.purple_bg, text="")
            self.logo_label.pack(side="left", padx=20, pady=10)
        except FileNotFoundError:
            self.logo_label = ctk.CTkLabel(self.top_bar_frame, text="LOGO", font=("THSarabun", 20), bg=self.purple_bg, fg=self.white_fg)
            self.logo_label.pack(side="left", padx=20, pady=10)
            print("Warning: hatyai_logo.png not found. Using text placeholder.")


        # App Title in header
        self.app_title_label = ctk.CTkLabel(self.top_bar_frame,
                                        text="AI-Powered Anti-trigger Fingers",
                                        font=self.font_large_title,
                                        text_color=self.white_fg,
                                        fg_color=self.purple_bg)
        self.app_title_label.pack(side="left", padx=20, pady=10)

        # --- Main Content Area ---
        self.main_content_frame = ctk.CTkFrame(self, fg_color=self.light_gray_bg_program)
        self.main_content_frame.pack(side="top", fill="both", expand=True, pady=20)

        # Configure grid layout (3 columns: left, middle, right)
        self.main_content_frame.grid_columnconfigure(0, weight=1, minsize=400) # Left image column
        self.main_content_frame.grid_columnconfigure(1, weight=1, minsize=350) # Middle text boxes/button
        self.main_content_frame.grid_columnconfigure(2, weight=1, minsize=300) # Right timer/image column
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(1, weight=1)
        self.main_content_frame.grid_rowconfigure(2, weight=1)

        # --- Robot Hand Image (Left) ---
        try:
            robot_hand_image_pil = Image.open("pictures/pose_1/1.jpg") # Assuming 'robot_hand.png'
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450), Image.LANCZOS) 
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.robot_hand_photo ,text="")
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew") 
        except FileNotFoundError:
            self.robot_hand_label = ctk.CTkLabel(self.main_content_frame, text="Robot Hand Image\n(Placeholder)",
                                            font=self.font_medium_text, bg="gray", fg="white", width=25, height=15)
            self.robot_hand_label.grid(row=0, column=0, rowspan=3, padx=40, pady=20, sticky="nsew")
            print("Warning: robot_hand.png not found. Using text placeholder.")

        # --- Middle Column: Sets & Rounds info ---
        self.set_times_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.light_gray_bg, border_width=1)
        self.set_times_frame.grid(row=0, column=1, padx=20, pady=10, sticky="ew") # Removed expand=True to control size

        # Round counter
        self.times_line_frame = ctk.CTkFrame(self.set_times_frame, fg_color=self.light_gray_bg)
        self.times_line_frame.pack(side="top", pady=(10,0))

        self.Label_times_text = ctk.CTkLabel(self.times_line_frame, text="ครั้งที่ : ", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_times_text.pack(side="left", padx=(10,0))

        self.Label_set_times_number = ctk.CTkLabel(self.times_line_frame, text=f"{self.round}", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_times_number.pack(side="left", padx=(0,10))

        # Set counter
        self.sets_line_frame = ctk.CTkFrame(self.set_times_frame, fg_color=self.light_gray_bg)
        self.sets_line_frame.pack(side="top", pady=(0,10)) # Padding only bottom

        self.Label_set_text = ctk.CTkLabel(self.sets_line_frame, text="เซ็ตที่ : ", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_text.pack(side="left", padx=(10,0))

        self.Label_set_number = ctk.CTkLabel(self.sets_line_frame, text=f"{self.set}", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_number.pack(side="left", padx=(0,10))


        # --- Pose Text ---
        self.pose_text_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.light_gray_bg, border_width=1)
        self.pose_text_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.Label_pose_thai_text = ctk.CTkLabel(self.pose_text_frame, text=f"ท่าที่ {self.current_pose}", font=self.font_pose_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_pose_thai_text.pack(side="top", pady=(10,0))
        
        self.Label_pose_action_text = ctk.CTkLabel(self.pose_text_frame, text=f"{self.pose_name[self.current_pose]}", font=self.font_pose_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_pose_action_text.pack(side="top", pady=(0,10))

        # --- Control Buttons (Start/Pause, Reset) ---
        self.buttons_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.light_gray_bg_program)
        self.buttons_frame.grid(row=2, column=1, columnspan=2, padx=(10),pady=(10, 20), sticky="ew") 

        # --- Start/Pause ---
        self.start_stop_button = ctk.CTkButton(self.buttons_frame, text="เริ่มต้น", font=("TH Sarabun", 50 ,"bold"), 
        fg_color=self.green_btn, text_color=self.white_fg, 
        command=self.toggle_start_pause, height=80, width=200, hover_color=self.hover_green_bt); self.start_stop_button.pack(side="left", padx=0)
        
        # --- Reset ---
        self.reset_button = ctk.CTkButton(self.buttons_frame, text="รีเซ็ต", font=("TH Sarabun", 50 ,"bold"),
        fg_color=self.red_btn, text_color=self.white_fg, 
        command=self.reset_action, height=80, width=200,hover_color=self.hover_red_bt); self.reset_button.pack(side="left", padx=10)

        # --- Timer Circle (Right Top) ---
        self.timer_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.white_fg)
        self.timer_frame.grid(row=0, column=2, padx=20, pady=20, sticky="n") # Sticky "n" to align to top

        self.timer_canvas = ctk.CTkCanvas(self.timer_frame, width=200, height=200, bg=self.white_fg, highlightthickness=0)
        self.timer_canvas.pack()

        self.timer_canvas.create_oval(10, 10, 190, 190, outline="#3CB371", width=10,tags="progress") # MediumSeaGreen
        self.timer_text = self.timer_canvas.create_text(100, 100, text=f"{self.time_current}", font=self.font_timer, fill=self.black_fg)

        # --- Small Pose Image (Right Bottom) ---
        try:
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose1.png") # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200), Image.LANCZOS)
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, image=self.small_hand_photo, text="")
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0,20), sticky="n") 
        except FileNotFoundError:
            self.small_hand_label = ctk.CTkLabel(self.main_content_frame, text="Small Hand\nImage\n(Placeholder)",
                                            font=("THSarabun", 16), bg="lightgray", width=15, height=10)
            self.small_hand_label.grid(row=1, column=2, padx=20, pady=(0,20), sticky="n")
            print("Warning: small_hand.png not found. Using text placeholder.")
            
        # --- log ---
        self.log_button = ctk.CTkButton(self.buttons_frame,text="รายงาน",font=("TH Sarabun", 50 ,"bold"),fg_color="#4285F4",text_color=self.white_fg,
        command=self.show_history_page,height=80, width=200,hover_color="#3367D6")
        self.log_button.pack(side="right", padx=100)
        
        # --- History Page ---
        self.history_page = ctk.CTkFrame(self, fg_color=self.light_gray_bg_program)

        self.history_title = ctk.CTkLabel(self.history_page, text="รายงานย้อนหลัง",font=("TH Sarabun", 55 ,"bold"), text_color=self.black_fg)
        self.history_title.pack(pady=20)

        self.history_textbox = ctk.CTkTextbox(self.history_page, width=1000, height=500,font=("TH Sarabun", 28 ,"bold"), text_color=self.black_fg)
        self.history_textbox.pack(padx=40, pady=20)

        self.back_button = ctk.CTkButton(self.history_page, text="กลับ",font=("TH Sarabun", 50 ,"bold"), fg_color="#FF9800",text_color="white", hover_color="#E68900",
        command=self.show_main_page, height=70, width=200)
        self.back_button.place(x=900, y=500)


        #senser loop
        self.running = False
        self.check_sensor_loop()
        
        self.pose_sounds = {
            1: ["001.mp3"],
            2: ["002.mp3"],
            3: ["003.mp3"],
            4: ["004.mp3"],
            5: ["005.mp3"]
        }
        
        
    def play_sounds_sequential(self, filenames):
        def _play_sequence():
            filename = f"Voices/{filenames}"
            try:
                print(f"[Sound] Playing: {filename}")
                playsound(filename)
            except Exception as e:
                print(f"Sound error: {e}")
        threading.Thread(target=_play_sequence, daemon=True).start()

    # def play_sound_thread(self, filename):
    #     def _play():
    #         try:
    #             pygame.mixer.music.load(filename)
    #             pygame.mixer.music.play()   
    #             while pygame.mixer.music.get_busy():
    #                 pygame.time.wait(100)
    #         except Exception as e:
    #             print(f"Sound error: {e}")
    #     threading.Thread(target=_play, daemon=True).start()

        
        # log page
    def load_history(self):
        try:
            with open("Anti-Finger.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = ["No history found.\n"]

        max_lines = 13
        if len(lines) > max_lines:
            lines = lines[-max_lines:]

        # clear textbox
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")
        self.history_textbox.insert("end", "".join(lines))
        self.history_textbox.see("end")
        self.history_textbox.configure(state="disabled")

        # recall 2 sec
        self.after(2000, self.load_history)
        
        # show main when dont click log
    def show_main_page(self):
        self.history_page.pack_forget()
        self.main_content_frame.pack(side="top", fill="both", expand=True, pady=20)
        self.play_sounds_sequential("010.mp3")
        # show log when click
    def show_history_page(self):
        self.main_content_frame.pack_forget()
        self.play_sounds_sequential("009.mp3")
        self.history_page.pack(side="top", fill="both", expand=True, pady=20)
        self.load_history()
        

        #log text setting
    def write_log(self, message):
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_message = f"{now} เซ็ตที่ {self.set} ครั้งที่ {self.round} : {message}"
        
        with open("Anti-Finger.txt", "a", encoding="utf-8") as f:
            f.write(log_message + "\n") 
        
        print(log_message)
    
        # Read values from MCP3008 (5 channels = 5 fingers)
    def check_fingers(self):
        values = [self.mcp.read_adc(i) for i in range(5)]
        print(f"Reading MCP3008 values: {values}")
        if values[0] <= 500 and all(v <= 50 for v in values[1:]):
            print("[Debug] : Pose condition met!")

        # Reset timer back to max/hand position
    def timer_reset(self):
        self.time_current = self.time_max
        self.hand_posit = 0
        self.update_timer()
        self.reset_pic()
        print("[Debug] : Timer reset!")
        print(f"[Debug] : Hand position reset to {self.hand_posit}")

        
        # Load robot hand image according to current pose and hand position
    def update_pic(self):
        pose_folder = f"pictures/pose_{self.current_pose}"
        try:
            robot_hand_image_pil = Image.open(f"{pose_folder}/{self.hand_posit}.jpg")
            robot_hand_image_pil = robot_hand_image_pil.resize((400, 450))
            self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
            self.robot_hand_label.configure(image=self.robot_hand_photo)
        except FileNotFoundError:
            print(f"[Debug] : Image for pose {self.current_pose}, hand {self.hand_posit} not found")

        # Reset image to default pose_1
    def reset_pic(self): 
        robot_hand_image_pil = Image.open(f"pictures/pose_1/1.jpg")  # Assuming 'robot_hand.png'
        robot_hand_image_pil = robot_hand_image_pil.resize((400, 450))  # Adjust size as needed
        self.robot_hand_photo = ImageTk.PhotoImage(robot_hand_image_pil)
        self.robot_hand_label.configure(image=self.robot_hand_photo)
        # Reset progress bar (circle)
        self.timer_canvas.delete("progress")
        self.timer_canvas.create_oval(10, 10, 190, 190, outline="#3CB371", width=10, tags="progress")

        # Update the timer UI
    def update_timer(self): 
        if self.time_current > 0:
            self.progress = (self.time_max - self.time_current) / self.time_max
            self.extent = 360 * self.progress
            print(f"[Debug] : Timer : {self.time_current}")
            self.timer_canvas.delete("progress")
            self.timer_canvas.itemconfig(self.timer_text, text=self.time_current)
            self.timer_canvas.create_arc(10, 10, 190, 190,start=90,outline="#3CB371", width=10,extent=-self.extent,style="arc",tags="progress")
        else:
            print(f"[Debug] : Timer : {self.time_current}")
            self.timer_canvas.itemconfig(self.timer_text, text=self.time_current)
            self.timer_canvas.delete("progress")
            self.timer_canvas.create_oval(10, 10, 190, 190, outline="#3CB371", width=10, tags="progress")

        # Update round/set labels
    def update_round(self):
        self.Label_set_times_number.configure(text=self.round)
        self.Label_set_number.configure(text=self.set)

        # Update example pose (EX_POSE) image according to current pose
    def update_EX_pose(self):
        if self.current_pose == 1:
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose1.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200))  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label.configure(image=self.small_hand_photo)
        elif self.current_pose == 2:
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose2.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200))  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label.configure(image=self.small_hand_photo)
        elif self.current_pose == 3:
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose3.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200))  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label.configure(image=self.small_hand_photo)
        elif self.current_pose == 4:
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose4.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200))  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label.configure(image=self.small_hand_photo)
        elif self.current_pose == 5:
            small_hand_image_pil = Image.open("pictures/EX_POSE/pose5.png")  # Assuming 'small_hand.png'
            small_hand_image_pil = small_hand_image_pil.resize((200, 200))  # Adjust size
            self.small_hand_photo = ImageTk.PhotoImage(small_hand_image_pil)
            self.small_hand_label.configure(image=self.small_hand_photo)
        else:
            print("[Debug] Out of bound!")

        # Update pose text
    def update_text(self):
        self.Label_pose_thai_text.configure(text=f"ท่าที่ {self.current_pose}")
        self.Label_pose_action_text.configure(text=f"{self.pose_name[self.current_pose] }")

        # Countdown before starting
    def start_pose_countdown(self, count=2):
        if count > 0:
            print(f"[Countdown] : {count}")
            self.after(1000, self.start_pose_countdown, count-1)
        else:
            print("[Debug] : Go!")
            self.hand_posit = 0
            self.time_current = self.time_max
            self.update_timer()
            self.check_sensor_loop()
 
        # Dictionary of sensor ranges from MCP3008 for each pose
    gestures = {
        1: [(0,999), (0,600), (0,600), (0,600), (0,800)],
        2: [(0,999), (870,999), (870,999), (870,999), (670,999)],
        3: [(0,999), (900,999), (900,999), (900,999), (750,999)],
        4: [(0,999), (200,999), (350,999), (350,999), (220,999)],
        5: [(0,999), (0,600), (0,600), (0,600), (0,900)],
    }
    
        # Loop to check values from sensors
    def check_sensor_loop(self):
        if self.running:
            values = [self.mcp.read_adc(i) for i in range(5)]
            print(f"[Debug] Sensor values: {values}")
            ranges = self.gestures.get(self.current_pose)
            pose_ok = all(low <= val <= high for val, (low, high) in zip(values, ranges))

            if pose_ok:
                if self.hand_posit < 5:
                    self.hand_posit += 1
                    self.update_pic()

                if self.hand_posit == 5 and self.time_current > 0 and not self.still_hold:
                    self.time_current -= 1
                    self.update_timer()
                if self.time_current <= 0:
                    self.write_log(f"ท่า{self.pose_name[self.current_pose]}สําเร็จ!")
                    self.current_pose += 1
                    if self.current_pose > 5:
                        self.current_pose = 1
                        self.round += 1
                        if self.round >= 10:
                            self.round = 0
                            self.set += 1
                        self.update_round()

                    self.timer_reset()
                    self.update_EX_pose()
                    self.update_text()
                    self.play_sounds_sequential(f"{self.pose_sounds[self.current_pose]}.mp3")
            self.after(1000, self.check_sensor_loop)

        # Reset all values to default
    def reset_action(self):
        print("[Debug] : Reset action")
        self.play_sounds_sequential("008.mp3")
        # reset value
        self.round = 0
        self.set = 0
        self.current_pose = 1
        self.hand_posit = 0
        self.time_current = self.time_max
        self.is_pass = False
        self.still_hold = False
        self.running = False   # reset state

        # reset UI
        self.reset_pic()
        self.update_timer()
        self.update_round()
        self.update_EX_pose()
        self.update_text()

        # reset Start/Stop button
        self.start_stop_button.configure(
            text="เริ่มต้น",
            fg_color=self.green_btn,
            hover_color=self.hover_green_bt
        )

    def toggle_start_pause(self):
        if self.start_stop_button.cget("text") == "เริ่มต้น":
            self.start_stop_button.configure(text="หยุด",fg_color=self.yellow_btn,hover_color=self.hover_yellow_bt)
            self.running = True
            self.start_pose_countdown(2)
            self.play_sounds_sequential("006.mp3")
        else:
            self.start_stop_button.configure(text="เริ่มต้น",fg_color=self.green_btn,hover_color=self.hover_green_bt)
            self.running = False
            self.play_sounds_sequential("007.mp3")

# Function to create dummy images for testing (if real images are missing)
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
