import tkinter as tk
import math
import gpsd
import time

UPDATE_INTERVAL = 200
MAX_SPEED = 50
ARC_COLOR = "green"

try:
	gpsd.connect()
	print("Connected to GPSD")
except Exception as e:
	print("Failed to Connect to GPSD:", e)
exit()

root = tk.TK()
root.title("GPS Speedometer")
root.geometry("400x300")
root.configure(bg="black")

canvas = tk.Canvas(root, width=400, height=300, bg="black", highlightthickness=0)
canvas.pack()

def draw_speedometer(speed_mpph):
	canvas.delete("all")
	cx, cy = 200, 200
	r=150

canvas.create_arc(cx-r, cy-r, cx+r, start=180, extent = 180,
outline="#333", width=20, style="arc")

extent = min((speed_mph / MAX_SPEED) * 180, 180)
canvas.create_arc(cx-r, cy-r, cx+r, start=180, extent=extent,
outline=ARC_COLOR, width=20, style="arc")

canvas.create_text(cx, cy-20, text=f"{int(speed_mph)}", fill="white", font=("Helvetica", 10))

def update_speed():
	try:
		packet = gpsd.get_current()
		if packet.mode >= 2:
			speed_mph = packet.speed()*0.621371
		else:
			speed_mph = 0.0
	except Exception as e:
		print("Error reading GPS:", e)
		speed_mph = 0.0

draw_speedometer(speed_mph)
root.after(UPDATE_INTERVAL, update_speed)

update.speed()
root.mainloop()

