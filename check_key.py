import tkinter as tk
from time import sleep

def key_press(event):
    key = event.char
    if key == "1":
        for i in range(1,6):
            print(f"[Debug] from 1 : {i}")
            sleep(1)
    elif key == "2":
        for i in range(1,6):
            print(f"[Debug] from 2 : {i}")
            sleep(1)



root = tk.Tk()
root.geometry('640x480')
root.bind('<Key>', key_press)
root.mainloop()