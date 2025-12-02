import tkinter as tk
import gpsd
import time

# Connect to GPSD
try:
    gpsd.connect()
    print("Connected to GPSD")
except Exception as e:
    print("Could not connect to GPSD:", e)
    exit()

# Create window
root = tk.Tk()
root.title("GPS Speedometer")
root.geometry("300x200")
root.configure(bg="black")

# Speed label
speed_label = tk.Label(root, text="0.0 mph", font=("Helvetica", 48), fg="lime", bg="black")
speed_label.pack(expand=True)

def update_speed():
    try:
        packet = gpsd.get_current()
        if packet.mode >= 2:
            # Convert m/s → mph
            speed_mph = packet.speed() * 2.23694
        else:
            speed_mph = 0.0
    except Exception as e:
        print("Error reading GPS:", e)
        speed_mph = 0.0

    speed_label.config(text=f"{speed_mph:4.1f} mph")
    root.after(500, update_speed)

update_speed()
root.mainloop()
