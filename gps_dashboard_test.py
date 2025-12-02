import tkinter as tk
import random

# ---------- CONFIG ----------
FAKE_MODE = True   # True = simulate speed, False = use real GPS
UPDATE_INTERVAL = 100  # milliseconds

MAX_SPEED = 60  # max speed for bar, adjust as needed

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Digital Speedometer")
root.geometry("480x320")  # Adjust for your 5" display
root.configure(bg="black")

# ---------- SPEED VARIABLES ----------
speed_mph = 0
target_speed = 0

# ---------- LABEL FOR SPEED ----------
speed_label = tk.Label(root, text="0 mph", font=("Helvetica", 72), fg="lime", bg="black")
speed_label.pack(pady=20)

# ---------- SPEED BAR ----------
canvas = tk.Canvas(root, width=400, height=30, bg="grey20", highlightthickness=0)
canvas.pack()
speed_bar = canvas.create_rectangle(0, 0, 0, 30, fill="lime")

# ---------- UPDATE FUNCTION ----------
def update_speed():
    global speed_mph, target_speed
   
    # --- get new speed ---
    if FAKE_MODE:
        # Simulate speed changes
        target_speed += random.uniform(-3, 3)
        target_speed = max(0, min(target_speed, MAX_SPEED))
    else:
        # TODO: replace with real GPS reading
        # Example: target_speed = gps_reading_from_module * 2.23694
        pass
   
    # Smooth the speed
    speed_mph += (target_speed - speed_mph) * 0.2
   
    # Update label
    speed_label.config(text=f"{int(speed_mph)} mph")
   
    # Update bar
    bar_length = (speed_mph / MAX_SPEED) * 400
    canvas.coords(speed_bar, 0, 0, bar_length, 30)
   
    # Change color based on speed
    if speed_mph < MAX_SPEED * 0.5:
        canvas.itemconfig(speed_bar, fill="lime")
    elif speed_mph < MAX_SPEED * 0.8:
        canvas.itemconfig(speed_bar, fill="yellow")
    else:
        canvas.itemconfig(speed_bar, fill="red")
   
    # Schedule next update
    root.after(UPDATE_INTERVAL, update_speed)

# ---------- START UP ----------
update_speed()
root.mainloop()
