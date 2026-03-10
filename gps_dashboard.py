import tkinter as tk
import random

#create a window
root = tk.Tk()
root.title("Digital Speedometer")
root.geometry("400x200") #adjust for 5" display

speed_mph = 0

#label to display speed
speed_label = tk.Label(root, text="0 mph", font=("Helvetica", 48))
speed_label.pack(expand=True)

def update_speed():
	global speed_mph
#Simulate speed changes
speed_mph += random.uniform(-2, 2)
speed_mph = max(0, speed_mph)
speed_label.config(text=f"{speed_mph:.1f} mph")
root.after(200, update_speed) #update every .2 seconds

update_speed()
root.mainloop()
