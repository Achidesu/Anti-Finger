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

        #event
        self.key_held = False

        #keybind
        self.bind("<Key-1>", self.on_key_press)
        self.bind("<KeyRelease-1>", self.on_key_release)

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
            robot_hand_image_pil = Image.open("pictures/pose_1/01.jpg") # Assuming 'robot_hand.png'
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

        self.Label_set_times_number = ctk.CTkLabel(self.times_line_frame, text="1", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_times_number.pack(side="left", padx=(0,10))

        # Inner frame to keep เซ็ต and number on the same line
        self.sets_line_frame = ctk.CTkFrame(self.set_times_frame, fg_color=self.light_gray_bg)
        self.sets_line_frame.pack(side="top", pady=(0,10)) # Padding only bottom

        self.Label_set_text = ctk.CTkLabel(self.sets_line_frame, text="เซ็ตที่ : ", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_text.pack(side="left", padx=(10,0))

        self.Label_set_number = ctk.CTkLabel(self.sets_line_frame, text="1", font=self.font_medium_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_set_number.pack(side="left", padx=(0,10))


        # --- Pose Text (Middle Column, Middle) ---
        self.pose_text_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.light_gray_bg, border_width=1)
        self.pose_text_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.Label_pose_thai_text = ctk.CTkLabel(self.pose_text_frame, text="ท่าที่ 1", font=self.font_pose_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_pose_thai_text.pack(side="top", pady=(10,0))
        self.Label_pose_action_text = ctk.CTkLabel(self.pose_text_frame, text="กำมือ", font=self.font_pose_text, text_color=self.black_fg, fg_color=self.light_gray_bg)
        self.Label_pose_action_text.pack(side="top", pady=(0,10))


        # --- Reset Button (Middle Column, Bottom) ---
        self.reset_button = ctk.CTkButton(self.main_content_frame, text="Reset", font=("Sarabun",20),
                                      fg_color=self.red_btn, text_color=self.white_fg,
                                      command=self.say,
                                      height=50, width=200, hover_color=self.hover_red_bt) # Adjust button size
        self.reset_button.grid(row=2, column=1, padx=20, pady=(10,20), sticky="n") # Align to top of its cell


        # --- Timer Display (Right Column, Top) ---
        self.timer_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.white_fg)
        self.timer_frame.grid(row=0, column=2, padx=20, pady=20, sticky="n") # Sticky "n" to align to top

        # Create a canvas to draw the circle
        self.timer_canvas = ctk.CTkCanvas(self.timer_frame, width=200, height=200, bg=self.white_fg, highlightthickness=0)
        self.timer_canvas.pack()

        # Draw the circle (x1, y1, x2, y2)
        self.timer_canvas.create_oval(10, 10, 190, 190, outline="#3CB371", width=10) # MediumSeaGreen
        self.timer_text = self.timer_canvas.create_text(100, 100, text="5s", font=self.font_timer, fill=self.black_fg)


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

    def on_key_press(self, event=None):
        if not self.key_held:
            self.key_held = True
            self.check_key_loop()

    def on_key_release(self, event=None):
        self.key_held = False

    def check_key_loop(self):
        if self.key_held:
            print("hold")
            self.after(1000, self.check_key_loop)
        else:
            print("release")

    def say(self):
        print("reset")




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