import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Full Circle Arc")

# Create a Canvas widget
canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack()

# Define the bounding box for the oval (which will be a circle if square)
# (x1, y1) is the top-left corner, (x2, y2) is the bottom-right corner
x1, y1 = 50, 50
x2, y2 = 150, 150
coordinates = (x1, y1, x2, y2)

# Create a full circle using create_arc
# Set start=0 (or any angle) and extent=360 to draw a complete circle
canvas.create_arc(coordinates, start=0, extent=360, fill="blue", outline="black", width=2)

# Run the Tkinter event loop
root.mainloop()