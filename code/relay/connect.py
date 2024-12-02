import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import serial
import time
from ewma import EWMA
from datetime import datetime

import threading
import queue

THRESHOLD = 3
MAX_DISTANCE = 30
GRACE_PERIOD = 20 # After placing the phone down, the user has 20 seconds to pick it back up. 
 
update_queue = queue.Queue()  # To send updates to the GUI

# Set up the serial connection
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)  # Replace with your port (e.g., COM3 for Windows)

time.sleep(1)  # Give Arduino time to initialize

# Function to send and receive data
def send_receive(data):
    arduino.write(f"{data}\n".encode())  # Send data as bytes
    time.sleep(0.05)                      # Wait for a response
    response = arduino.readline().decode().strip()  # Read response
    return response


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
distraction_label = ttk.Label(frame_top, text=f"Distractions: 0", font=("Arial", 16))
distraction_label.pack(side=tk.RIGHT, padx=10)

time_label = ttk.Label(frame_top, text=f"Remaining Time: 0", font=("Arial", 16))
time_label.pack(side=tk.LEFT, padx=10)

# Create plot figure
fig, ax = plt.subplots()
line_actual, = ax.plot([], [], label="Completed Time", color="blue")
line_predicted, = ax.plot([], [], label="Suggested Time", color="orange")
ax.set_title("Suggested Time vs Completed Focus Sessions")
ax.set_xlabel("Time")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True)

# Embed the plot in Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)


def update_plot(ewma):
    """Update the EWMA plot with the latest data."""
    actual_data, predicted_data = ewma.actual[1:], ewma.predicted[:-1]
    print("Actual data:", actual_data)
    print("Predicted data:", predicted_data)

    # Update plot data
    line_actual.set_data(range(len(actual_data)), actual_data)
    line_predicted.set_data(range(len(predicted_data)), predicted_data)

    # Adjust axis limits dynamically
    ax.set_xlim(0, max(len(actual_data), len(predicted_data)))
    ax.set_ylim(0, max(max(actual_data, default=1), max(predicted_data, default=1)))
    # Redraw canvas
    canvas.draw()


off_stand_time = None

def send_rgb(r, g, b, intensity=1):
    """Send RGB values to the Arduino."""
    r = int(r * intensity)
    g = int(g * intensity)
    b = int(b * intensity)
    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
        rgb_data = f"{r},{g},{b}\n"  # Format as 'R,G,B\n'
        arduino.write(rgb_data.encode())  # Send data to Arduino
        # print(f"Sent: {rgb_data.strip()}")
    else:
        print("Error: RGB values must be between 0 and 255.")

def clear_led():
    """Turn off the LED."""
    send_rgb(0, 0, 0)


def blink_led(color):
    """Blink the LED."""
    for _ in range(3):
        send_rgb(color[0], color[1], color[2])
        time.sleep(0.5)
        clear_led()


def pulse_led(color):
    r,g,b = color

    for i in range(0,100, 5):
        send_rgb(r, g, b, i/100)
        time.sleep(0.005)

    for i in range(100, 0, -5):
        send_rgb(r, g, b, i/100)
        time.sleep(0.005)


# Handle GUI close event
def on_close():
    """Handle program closing."""
    arduino.close()
    root.destroy()


def gui_update():
    """Process updates from the queue and refresh the GUI."""
    while not update_queue.empty():
        message = update_queue.get()

        if message.get("type") == "distraction":
            distraction_label.config(text=f"Distractions: {message['value']}")

        if message.get("type") == "time":
            time_label.config(text=f"Time remaining: {message['value']}")

        if message.get("type") == "plot":
            ewma = message["value"]
            update_plot(ewma)


    # Schedule the next check
    root.after(100, gui_update)

# Example usage
def arduino_thread():

    ewma = EWMA()
    focus_start = None
    focusing = False
    session_length = 10
    decrease_time = time.time()
    distractions = 0
    distracted = False
    finished = False
    end_time = None

    try:
        clear_led()
        print("Starting!")
        while True:

            current_time = time.time()
            distance = float(arduino.readline().decode().strip())

            # Check if the session has ended
            if focus_start is not None and focusing and distance < THRESHOLD:
                time_diff = datetime.now() - focus_start
                if time_diff.total_seconds() >= session_length:
                    print("Focus session complete!")

                    focusing = False
                    focus_start = None
                    distracted = False
                    off_stand_time = None
                    finished = True

                    session_length = ewma.adjust(session_length)
                    update_queue.put({"type": "plot", "value": ewma})

                    print("Focus score: ", ewma.focus_score())
                    end_time = time.time()

                    # important to call these last!
                    pulse_led((255, 255, 255))
                    clear_led()
                    time.sleep(2)
                    continue 

            if end_time is not None and current_time - end_time >= 2:
                finished = False
                print("Restarting!")


            # Start a focus session if the phone is placed down
            if not finished and distance < THRESHOLD and not focusing and focus_start is None:

                if end_time is not None and current_time - end_time < 2:
                    print("Please wait 5 seconds before starting a new session.")
                    continue

                if len(ewma.actual) == 0:
                    session_length = 5
                else:
                    session_length = ewma.adjust(session_length)
                    update_plot(ewma)

                print(f"Starting session for {session_length}")

                send_rgb(255, 255, 255)

                focus_start = datetime.now()

                focusing = True

            # Update the intensity of the LED
            if focusing and distance < THRESHOLD and current_time - decrease_time >= 1:
                time_diff = datetime.now() - focus_start
                print("time remaining: ", session_length - time_diff.total_seconds() // 1)

                update_queue.put({"type": "time", "value": session_length - time_diff.total_seconds() // 1})

                intensity = 1 - (time_diff.total_seconds() / session_length)
                send_rgb(255, 255, 255, intensity)

                decrease_time = time.time()

            # Need to make sure this doesn't constantly trigger.
            if focusing and distance < THRESHOLD and distracted:
                distracted = False
                distractions += 1
                update_queue.put({"type": "distraction", "value": distractions})
                print(f"Distraction detected! Total distractions: {distractions}")

            # The extra 1.5 factor is to help prevent false positives
            if focusing and distance > 3.2 and current_time - decrease_time >= 0.3 and not finished:

                if not off_stand_time:
                    off_stand_time = time.time()
                    send_rgb(255, 100, 0)
                    distracted = True
                    
                if current_time - off_stand_time >= 1:
                    print("You've moved your device, and your focus session is forfeit.")
                    focus_end = datetime.now()
                    duration = focus_end - focus_start

                    hours, remainder = divmod(duration.total_seconds(), 3600)
                    minutes, _ = divmod(remainder, 60)
                    print(f"Hours: {int(hours)}, Minutes: {int(minutes)}, Seconds: {duration.seconds % 60}")

                    ewma.adjust(duration.total_seconds())
                    update_queue.put({"type": "plot", "value": ewma})

                    # Blink the LEDs to indicate the session is over.
                    pulse_led((255, 0, 0))

                    # End the focus session
                    focusing = False
                    focus_start = None
                    clear_led()

            else:
                off_stand_time = None



    except KeyboardInterrupt:
        print("Program interrupted!")

    finally:
        arduino.close()  # Close the connection


athread = threading.Thread(target=arduino_thread, daemon=True)
athread.start()


root.protocol("WM_DELETE_WINDOW", on_close)

gui_update()

# Start the Tkinter event loop
root.mainloop()
