import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class CountdownTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer with Graph")

        self.time_var = tk.StringVar(value="30")  # Default countdown time in seconds
        self.completed_times = []  # Store completed countdown times

        # Input Section
        ttk.Label(root, text="Enter countdown time (seconds):").pack(pady=5)
        self.time_entry = ttk.Entry(root, textvariable=self.time_var, width=10)
        self.time_entry.pack(pady=5)

        # Buttons
        self.start_button = ttk.Button(root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(root, text="Stop Timer", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Timer Display
        self.timer_label = ttk.Label(root, text="Time Remaining: 0", font=("Arial", 16))
        self.timer_label.pack(pady=10)

        # Graph Area
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.ax.set_title("Completed Countdown Times")
        self.ax.set_xlabel("Attempts")
        self.ax.set_ylabel("Seconds")
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

        self.timer_running = False
        self.remaining_time = 0

    def start_timer(self):
        try:
            self.remaining_time = int(self.time_var.get())
            if self.remaining_time <= 0:
                raise ValueError("Time must be positive.")
        except ValueError:
            self.timer_label.config(text="Invalid time entered!")
            return

        self.timer_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_timer()

    def update_timer(self):
        if self.timer_running and self.remaining_time > 0:
            self.timer_label.config(text=f"Time Remaining: {self.remaining_time}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.timer_label.config(text="Time's up!")
            self.completed_times.append(int(self.time_var.get()))
            self.update_graph()
            self.reset_buttons()

    def stop_timer(self):
        self.timer_running = False
        self.timer_label.config(text="Timer stopped!")
        self.reset_buttons()

    def reset_buttons(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_graph(self):
        self.ax.clear()
        self.ax.plot(self.completed_times, marker="o")
        self.ax.set_title("Completed Countdown Times")
        self.ax.set_xlabel("Attempts")
        self.ax.set_ylabel("Seconds")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimerApp(root)
    root.mainloop()
