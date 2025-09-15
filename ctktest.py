import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class KeyPressApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Key Hold Detection Example")
        self.geometry("400x300")

        # Track whether the key is being held down
        self.key_held = False

        # Example button to show other controls still work
        self.button = ctk.CTkButton(self, text="Click Me", command=self.say_hello)
        self.button.pack(pady=20)

        # Bind key press and release
        self.bind("<space>", self.on_key_press)
        self.bind("<KeyRelease-space>", self.on_key_release)

        # Label to show feedback
        self.label = ctk.CTkLabel(self, text="Press and hold SPACE")
        self.label.pack(pady=20)

    def say_hello(self):
        self.label.configure(text="Button clicked!")

    def on_key_press(self, event=None):
        if not self.key_held:  # Start loop only if not already running
            self.key_held = True
            self.check_key_loop()

    def on_key_release(self, event=None):
        self.key_held = False  # Stop the loop

    def check_key_loop(self):
        """This function keeps running while the key is held."""
        if self.key_held:
            self.label.configure(text="SPACE is being held!")
            # Run this again after 100ms
            self.after(100, self.check_key_loop)
        else:
            self.label.configure(text="SPACE released")

if __name__ == "__main__":
    app = KeyPressApp()
    app.mainloop()
