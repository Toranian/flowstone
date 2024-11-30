import dearpygui.dearpygui as dpg
from math import sin

dpg.create_context()

# Data for the plot
data = []

# Function to update the plot data
def update_plot_data(sender, app_data, plot_data):
    mouse_y = app_data[1]
    if len(plot_data) > 100:
        plot_data.pop(0)
    plot_data.append(sin(mouse_y / 30))
    dpg.set_value("plot", plot_data)

# Countdown timer logic
def update_timer(sender, app_data, user_data):
    # Check if timer is active before updating
    if user_data["active"]:
        if user_data["time_left"] > 0:
            user_data["time_left"] -= 1
            dpg.set_value("timer_label", f"Time Left: {user_data['time_left']}s")
        else:
            # Timer has completed
            dpg.set_value("timer_label", "Time's up!")
            user_data["active"] = False
            dpg.configure_item("start_button", label="Start Countdown")

def start_countdown(sender, app_data, user_data):
    # If timer is not already running
    if not user_data["active"]:
        input_time = dpg.get_value("time_input")
        try:
            countdown_time = int(input_time)
            if countdown_time > 0:
                user_data["time_left"] = countdown_time
                user_data["active"] = True
                dpg.set_value("timer_label", f"Time Left: {countdown_time}s")
                dpg.configure_item("start_button", label="Running...")
                
                # Create a timer that updates every second
                with dpg.timer(1.0, tag="timer_update", callback=update_timer, user_data=user_data):
                    pass
            else:
                dpg.set_value("timer_label", "Please enter a positive number.")
        except ValueError:
            dpg.set_value("timer_label", "Invalid input! Please enter a number.")
    else:
        # If timer is already running, allow cancellation
        user_data["active"] = False
        dpg.set_value("timer_label", "Countdown Stopped")
        dpg.configure_item("start_button", label="Start Countdown")
        dpg.delete_item("timer_update")

# Main Window
with dpg.window(label="Countdown Timer", width=500, height=500, tag='Primary Window'):
    # Simple plot (keeping the original functionality)
    dpg.add_simple_plot(label="Simple Plot", min_scale=-1.0, max_scale=1.0, height=300, tag="plot")
    
    # Timer input and controls
    dpg.add_input_text(label="Enter Countdown Time (s)", tag="time_input", width=200, default_value="10")
    dpg.add_button(
        label="Start Countdown", 
        tag="start_button",
        callback=start_countdown, 
        user_data={"time_left": 0, "active": False}
    )
    dpg.add_text("Time Left: 0s", tag="timer_label")

# Mouse move handler for plot updates
with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=update_plot_data, user_data=data)

# Setup Dear PyGui
dpg.create_viewport(title='Countdown Timer', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Primary Window', True)
dpg.start_dearpygui()
dpg.destroy_context()
