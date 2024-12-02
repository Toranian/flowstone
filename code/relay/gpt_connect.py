import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from ewma import EWMA
import serial
import time
from datetime import datetime

# Constants
THRESHOLD = 3
GRACE_PERIOD = 20  # After placing the phone down, user has 20 seconds to pick it back up.
SESSION_LENGTH = 10

# EWMA setup
ewma = EWMA()

# Arduino setup
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
time.sleep(1)  # Allow Arduino time to initialize

# Global variables
focusing = False
distractions = 0
focus_start = None
session_length = ewma.adjust(SESSION_LENGTH)
actual_data = []
predicted_data = []

# GUI setup
root = tk.Tk()
root.title("Focus Session Tracker")
root.geometry("800x600")

# Create frames
frame_top = ttk.Frame(root, padding="10")
frame_top.pack(fill=tk.X)

frame_plot = ttk.Frame(root, padding="10")
frame_plot.pack(fill=tk.BOTH, expand=True)

# Create distraction label
distraction_label = ttk.Label(frame_top, text=f"Distractions: {distractions}", font=("Arial", 16))
distraction_label.pack(side=tk.LEFT, padx=10)

# Create plot figure
fig, ax = plt.subplots()
line_actual, = ax.plot([], [], label="EWMA Actual", color="blue")
line_predicted, = ax.plot([], [], label="EWMA Predicted", color="orange")
ax.set_title("EWMA Actual vs Predicted")
ax.set_xlabel("Time")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True)

# Embed the plot in Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)


def update_plot():
    """Update the EWMA plot with the latest data."""
    global actual_data, predicted_data

    # Update plot data
    line_actual.set_data(range(len(actual_data)), actual_data)
    line_predicted.set_data(range(len(predicted_data)), predicted_data)

    # Adjust axis limits dynamically
    ax.set_xlim(0, max(len(actual_data), len(predicted_data)))
    ax.set_ylim(0, max(max(actual_data, default=1), max(predicted_data, default=1)))

    # Redraw canvas
    canvas.draw()


def monitor_arduino():


def on_close():
    """Handle program closing."""
    arduino.close()
    root.destroy()


# Start monitoring and updating
monitor_arduino()

# Handle GUI close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter event loop
root.mainloop()
