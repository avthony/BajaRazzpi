import tkinter as tk
import math
import random

# ---------- CONFIG ----------
FAKE_MODE = True
UPDATE_INTERVAL = 50  # ms
MAX_SPEED = 220  # Max speed for gauge
SPEED_RADIUS = 150

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Digital + Arc Speedometer")
root.geometry("400x300")
root.configure(bg="black")

# ---------- CANVAS ----------
canvas = tk.Canvas(root, width=400, height=300, bg="black", highlightthickness=0)
canvas.pack()

# ---------- SPEED VARIABLE ----------
speed = 0
target_speed = 0

# ---------- DRAW FUNCTION ----------
def draw_speedometer():
    canvas.delete("all")
    cx, cy = 200, 200  # center of arc
    r = SPEED_RADIUS
   
    # Draw background arc (semi-circle)
    canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=180, extent=180, outline="#333", width=20, style="arc")
   
    # Draw speed arc
    extent = (speed / MAX_SPEED) * 180
    canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=180, extent=extent, outline="orange", width=20, style="arc")
   
    # Draw digital speed
    canvas.create_text(cx, cy-20, text=f"{int(speed)}", fill="white", font=("Helvetica", 48))
    canvas.create_text(cx, cy+20, text="km/h", fill="white", font=("Helvetica", 16))
   
# ---------- UPDATE FUNCTION ----------
def update_speed():
    global speed, target_speed
    if FAKE_MODE:
        target_speed += random.uniform(-5, 5)
        target_speed = max(0, min(target_speed, MAX_SPEED))
    else:
        # Replace with real GPS speed in km/h
        # target_speed = gps_speed
        pass
   
    # Smooth speed transition
    speed += (target_speed - speed) * 0.2
   
    draw_speedometer()
    root.after(UPDATE_INTERVAL, update_speed)

# ---------- START ----------
update_speed()
root.mainloop()
