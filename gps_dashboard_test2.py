import tkinter as tk
import math
import random

# ---------- CONFIG ----------
FAKE_MODE = True
UPDATE_INTERVAL = 100  # ms
MAX_SPEED = 60
MAX_RPM = 8000

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Mini Car Dashboard")
root.geometry("480x320")
root.configure(bg="black")

# ---------- SPEED VARIABLES ----------
speed_mph = 0
target_speed = 0
rpm = 0
target_rpm = 0

# ---------- CANVASES ----------
canvas_left = tk.Canvas(root, width=150, height=150, bg="black", highlightthickness=0)
canvas_left.grid(row=0, column=0, padx=10, pady=10)

canvas_center = tk.Canvas(root, width=180, height=150, bg="black", highlightthickness=0)
canvas_center.grid(row=0, column=1, padx=10, pady=10)

canvas_right = tk.Canvas(root, width=150, height=150, bg="black", highlightthickness=0)
canvas_right.grid(row=0, column=2, padx=10, pady=10)

# ---------- DIGITAL SPEED LABEL ----------
speed_label = tk.Label(root, text="0 mph", font=("Helvetica", 36), fg="lime", bg="black")
speed_label.place(x=180, y=120)  # roughly centered

# ---------- FUNCTIONS ----------
def draw_gauge(canvas, value, max_value, label):
    canvas.delete("all")
    width = int(canvas['width'])
    height = int(canvas['height'])
    cx, cy = width // 2, height // 2
    radius = min(cx, cy) - 10
   
    # Draw gauge circle
    canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, outline="white", width=2)
   
    # Draw tick marks
    for i in range(0, max_value+1, max_value//6):
        angle = math.pi * (1 - i/max_value)  # 180 degrees arc
        x = cx + radius * 0.9 * math.cos(angle)
        y = cy - radius * 0.9 * math.sin(angle)
        canvas.create_line(cx, cy, x, y, fill="white", width=2)
   
    # Draw needle
    angle = math.pi * (1 - value/max_value)
    nx = cx + radius * 0.8 * math.cos(angle)
    ny = cy - radius * 0.8 * math.sin(angle)
    canvas.create_line(cx, cy, nx, ny, fill="red", width=3)
   
    # Label
    canvas.create_text(cx, cy+radius+15, text=label, fill="white", font=("Helvetica", 12))
    canvas.create_text(cx, cy, text=str(int(value)), fill="white", font=("Helvetica", 16))

def update_dashboard():
    global speed_mph, target_speed, rpm, target_rpm
   
    if FAKE_MODE:
        # Simulate speed
        target_speed += random.uniform(-2, 2)
        target_speed = max(0, min(target_speed, MAX_SPEED))
       
        # Simulate RPM
        target_rpm += random.uniform(-300, 300)
        target_rpm = max(0, min(target_rpm, MAX_RPM))
    else:
        # Replace with real GPS and RPM readings
        # target_speed = gps_reading_from_module * 2.23694
        # target_rpm = engine_rpm_reading
        pass
   
    # Smooth the values
    speed_mph += (target_speed - speed_mph) * 0.2
    rpm += (target_rpm - rpm) * 0.2
   
    # Update digital speed
    speed_label.config(text=f"{int(speed_mph)} mph")
   
    # Update analog gauges
    draw_gauge(canvas_left, speed_mph, MAX_SPEED, "Speed")
    draw_gauge(canvas_right, rpm, MAX_RPM, "RPM")
   
    root.after(UPDATE_INTERVAL, update_dashboard)

# ---------- START ----------
update_dashboard()
root.mainloop()
