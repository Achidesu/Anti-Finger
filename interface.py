import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import math
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

POSES = [
    ("ท่าที่ 1", "เหยียดมือตรง"),
    ("ท่าที่ 2", "ทำมือคล้ายตะขอ"),
    ("ท่าที่ 3", "กำมือ"),
    ("ท่าที่ 4", "กำมือแบบเหยียดปลายนิ้ว"),
    ("ท่าที่ 5", "งอโคนนิ้วแต่เหยียดปลายนิ้วมือ"),
]

POSE_IMAGES = [
    "pictures/pose1.png",
    "pictures/pose2.png",
    "pictures/pose3.png",
    "pictures/pose4.png",
    "pictures/pose5.png",
]


class ExerciseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI-Powered Anti-trigger Fingers")
        self.geometry("1280x800+0+0")

        # State
        self.current_pose = 0
        self.current_rep = 0
        self.current_set = 0
        self.time_left = 5.0
        self.max_time = 5.0
        self.running = False
        self.animation_running = True

        # Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # UI
        self.create_header()
        self.create_main_content()

        # Bind spacebar
        self.bind('<space>', self.toggle_exercise)

        # Start animation
        self.animate_timer()


    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#6A0DAD", height=150, corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_frame.grid_propagate(False)

        logo_frame = ctk.CTkFrame(header_frame, fg_color="white", width=50, height=50, corner_radius=25)
        logo_frame.place(x=30, y=15)

        title_logo = ImageTk.PhotoImage(Image.open("pictures/logo.png"))

        title_label = ctk.CTkLabel(
            header_frame,
            text="AI-Powered Anti-trigger Fingers",
            font=("Arial", 50, "bold"),
            text_color="white"
        )
        title_label.place(x=100, y=45)

    def create_main_content(self):
        # Left empty space
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=1, column=0, sticky="nsew")

        # Right panel
        right_frame = ctk.CTkFrame(self, fg_color="white", width=500, corner_radius=0)
        right_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid_propagate(False)

        content = ctk.CTkFrame(right_frame, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=40)

        # Stats card
        stats_frame = ctk.CTkFrame(content, fg_color="#f0f0f0", corner_radius=15)
        stats_frame.pack(fill="x", pady=(0, 30))

        # Round
        round_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        round_container.pack(fill="x", padx=30, pady=(20, 10))
        round_label = ctk.CTkLabel(round_container, text="ครั้งที่ :", font=("Arial", 24))
        round_label.pack(side="left")
        self.round_value = ctk.CTkLabel(round_container, text="0", font=("Arial", 28, "bold"))
        self.round_value.pack(side="right")

        # Set
        set_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        set_container.pack(fill="x", padx=30, pady=(10, 20))
        set_label = ctk.CTkLabel(set_container, text="เซ็ตที่ :", font=("Arial", 24))
        set_label.pack(side="left")
        self.set_value = ctk.CTkLabel(set_container, text="0", font=("Arial", 28, "bold"))
        self.set_value.pack(side="right")

        # Timer
        timer_frame = ctk.CTkFrame(content, fg_color="transparent")
        timer_frame.pack(pady=30)
        self.canvas = tk.Canvas(timer_frame, width=200, height=200, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_oval(10, 10, 190, 190, outline="#e0e0e0", width=12, tags="bg_circle")
        self.timer_text = self.canvas.create_text(100, 100, text="5s", font=("Arial", 48, "bold"), fill="#333")

        # Pose info
        pose_info_frame = ctk.CTkFrame(content, fg_color="transparent")
        pose_info_frame.pack(pady=20)
        self.pose_title = ctk.CTkLabel(pose_info_frame, text="ท่าที่ 1", font=("Arial", 32, "bold"))
        self.pose_title.pack()
        self.pose_desc = ctk.CTkLabel(pose_info_frame, text=POSES[0][1], font=("Arial", 24), text_color="#666")
        self.pose_desc.pack(pady=10)

        # Image
        self.left_frame = ctk.CTkFrame(self, fg_color="white", width=500, height=500, corner_radius=10)
        self.left_frame.grid(row=1, column=0, sticky="nsew", padx=70, pady=70)
        self.left_frame.grid_propagate(False)

        self.image_label = ctk.CTkLabel(self.left_frame, text="รูปท่าทาง", font=("Arial", 24), text_color="#999")
        self.image_label.pack(expand=True)

        # Reset
        self.reset_btn = ctk.CTkButton(content, text="Reset", font=("Arial", 20, "bold"),
                                       fg_color="#ff5252", hover_color="#ff1744",
                                       width=150, height=50, corner_radius=25,
                                       command=self.reset_exercise)
        self.reset_btn.pack(pady=20)

    def load_pose_image(self, index):
        path = POSE_IMAGES[index]
        if os.path.exists(path):
            img = Image.open(path)
            # ใช้ thumbnail เพื่อรักษาสัดส่วนไม่บีบ
            img.thumbnail((480, 480))  # ปรับขนาดให้ใหญ่ขึ้นตาม frame
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk, text="")
            self.image_label.image = img_tk
        else:
            self.image_label.configure(image=None, text=f"Pose {index + 1}")

    def animate_timer(self):
        if self.animation_running:
            self.canvas.delete("progress")
            if self.running and self.time_left > 0:
                progress = (self.max_time - self.time_left) / self.max_time
                extent = 360 * progress
                if extent > 0:
                    self.canvas.create_arc(10, 10, 190, 190, start=90, extent=-extent,
                                           outline="#2196F3", width=12, style="arc", tags="progress")
                self.canvas.itemconfig(self.timer_text, text=f"{int(self.time_left + 0.5)}s")
                self.time_left -= 0.1
                if self.time_left <= 0:
                    self.next_pose()
            else:
                self.canvas.itemconfig(self.timer_text, text=f"{int(self.max_time)}s")
            self.after(100, self.animate_timer)

    def toggle_exercise(self, event=None):
        self.running = not self.running
        if self.running and self.time_left <= 0:
            self.time_left = self.max_time

    def reset_exercise(self):
        self.running = False
        self.current_pose = 0
        self.current_rep = 0
        self.current_set = 0
        self.time_left = self.max_time
        self.round_value.configure(text="0")
        self.set_value.configure(text="0")
        self.pose_title.configure(text="ท่าที่ 1")
        self.pose_desc.configure(text=POSES[0][1])
        self.load_pose_image(0)
        self.canvas.delete("progress")

    def next_pose(self):
        self.current_pose += 1
        if self.current_pose >= len(POSES):
            self.current_pose = 0
            self.current_rep += 1
            self.round_value.configure(text=str(self.current_rep))
            if self.current_rep >= 10:
                self.current_rep = 0
                self.current_set += 1
                self.set_value.configure(text=str(self.current_set))

        self.pose_title.configure(text=f"ท่าที่ {self.current_pose + 1}")
        self.pose_desc.configure(text=POSES[self.current_pose][1])
        self.load_pose_image(self.current_pose)
        self.time_left = self.max_time

    def on_closing(self):
        self.animation_running = False
        self.destroy()


if __name__ == "__main__":
    app = ExerciseApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
