import tkinter as tk

def key_press(event):
    key = event.char
    print(f"'{key}' is pressed")


root = tk.Tk()
root.geometry('640x480')
root.bind('<Key>', key_press)
root.mainloop()