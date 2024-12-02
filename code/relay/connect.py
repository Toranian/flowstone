import serial
import time
from ewma import EWMA
from datetime import datetime

THRESHOLD = 3
MAX_DISTANCE = 30
GRACE_PERIOD = 20 # After placing the phone down, the user has 20 seconds to pick it back up. 
 

# Set up the serial connection
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)  # Replace with your port (e.g., COM3 for Windows)

time.sleep(1)  # Give Arduino time to initialize

# Function to send and receive data
def send_receive(data):
    arduino.write(f"{data}\n".encode())  # Send data as bytes
    time.sleep(0.05)                      # Wait for a response
    response = arduino.readline().decode().strip()  # Read response
    return response

focusing = False
distracted = False
ewma = EWMA()

session_length = ewma.adjust(10)
focus_start = None

decrease_time = time.time()

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

distractions = 0
# Example usage
try:
    clear_led()
    print("Starting!")
    while True:

        current_time = time.time()

        # Check if the session has ended
        if focus_start is not None and focusing:
            time_diff = datetime.now() - focus_start
            if time_diff.total_seconds() > session_length:
                print("Focus session complete!")

                focusing = False
                focus_start = None
                distracted = False

                session_length = ewma.adjust(session_length)

                # important to call these last!
                pulse_led((255, 255, 255))
                pulse_led((255, 255, 255))
                clear_led()


        distance = float(arduino.readline().decode().strip())

        # Start a focus session if the phone is placed down
        if distance < THRESHOLD and not focusing:

            if len(ewma.actual) == 0:
                session_length = 10
            else:
                session_length = ewma.adjust(session_length)

            print(f"Starting session for {session_length}")

            send_rgb(255, 255, 255)

            focus_start = datetime.now()

            focusing = True

        # Update the intensity of the LED
        if focusing and distance < THRESHOLD and current_time - decrease_time >= 1:
            time_diff = datetime.now() - focus_start
            print("time remaining: ", session_length - time_diff.total_seconds() // 1)

            intensity = 1 - (time_diff.total_seconds() / session_length)
            send_rgb(255, 255, 255, intensity)

            decrease_time = time.time()

        # Need to make sure this doesn't constantly trigger.
        if focusing and distance < THRESHOLD and distracted:
            distracted = False
            distractions += 1
            print(f"Distraction detected! Total distractions: {distractions}")

        # The extra 1.5 factor is to help prevent false positives
        if focusing and distance > 2.8:

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

                # Blink the LEDs to indicate the session is over.
                pulse_led((255, 0, 0))
                pulse_led((255, 0, 0))

                # End the focus session
                focusing = False
                # focus_start = None
                clear_led()



        else:
            off_stand_time = None



except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    arduino.close()  # Close the connection
