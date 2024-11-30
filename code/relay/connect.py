import serial
import time
from ewma import EWMA
from datetime import datetime

THRESHOLD = 3
MAX_DISTANCE = 6
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

distractions = 0
# Example usage
try:
    while True:

        current_time = time.time()

        if focus_start is not None and focusing:
            time_diff = datetime.now() - focus_start
            if time_diff.total_seconds() > session_length:
                print("Focus session complete!")
                blink_led((0, 0, 255))
                clear_led()

                focusing = False
                focus_start = None

                session_length = ewma.adjust(session_length)


        distance = float(arduino.readline().decode().strip())

        if distance < THRESHOLD and not focusing:
            focusing = True

            if len(ewma.actual) == 0:
                session_length = 10
            else:
                session_length = ewma.adjust(session_length)

            print(f"Starting session for {session_length}")

            send_rgb(0, 0, 255)

            focus_start = datetime.now()

        if focusing and distance < THRESHOLD and current_time - decrease_time >= 1:
            time_diff = datetime.now() - focus_start
            print("time remaining: ", session_length - time_diff.total_seconds() // 1)

            intensity = 1 - (time_diff.total_seconds() / session_length)
            send_rgb(255, 255, 255, intensity)

            decrease_time = time.time()

        # Need to make sure this doesn't constantly trigger.
        elif focusing and distance < THRESHOLD and distracted:
            blink_led((255, 255, 255))
            distracted = False
            distractions += 1
            print(f"Distraction detected! Total distractions: {distractions}")

        # The extra 1.5 factor is to help prevent false positives
        elif focusing and distance > THRESHOLD:


            if not off_stand_time:
                off_stand_time = time.time()
                send_rgb(255, 0, 0)
                
            if current_time - off_stand_time >= 3:
                print("You've moved your device, and your focus session is forfeit.")
                focus_end = datetime.now()
                duration = focus_end - focus_start

                hours, remainder = divmod(duration.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                print(f"Hours: {int(hours)}, Minutes: {int(minutes)}, Seconds: {duration.seconds % 60}")

                # Blink the LEDs to indicate the session is over.
                blink_led((255, 0, 0))

                # End the focus session
                focusing = False
                # focus_start = None
                clear_led()


            intensity = (distance / MAX_DISTANCE)
            send_rgb(255, 0, 0, intensity)
            distracted = True


except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    arduino.close()  # Close the connection
