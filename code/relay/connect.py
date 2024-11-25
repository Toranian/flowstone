import serial
import time
from ewma import EWMA
from datetime import datetime

THRESHOLD = 2.5

# Set up the serial connection
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)  # Replace with your port (e.g., COM3 for Windows)

time.sleep(1)  # Give Arduino time to initialize

# Function to send and receive data
def send_receive(data):
    arduino.write(f"{data}\n".encode())  # Send data as bytes
    time.sleep(0.5)                      # Wait for a response
    response = arduino.readline().decode().strip()  # Read response
    return response

focusing = False
ewma = EWMA()

session_length = 10
focus_start = datetime.now()

# Example usage
try:
    while True:
        # # user_input = input("Enter a message to send to Arduino: ")
        # # if user_input.lower() == "exit":
        # #     print("Exiting...")
        # #     break
        #
        # response = send_receive(user_input)
        # print(f"Arduino says: {response}")

        distance = float(arduino.readline().decode().strip())

        if distance < THRESHOLD and not focusing:
            print("In condition")
            focusing = True

            if len(ewma.actual) == 0:
                session_length = 10
            else:
                session_length = ewma.adjust(session_length)

            print(f"Starting session for {session_length}")

            focus_start = datetime.now()

        elif focusing and distance > 30:
            print("You've moved your device, and your focus session is forfeit.")
            focus_end = datetime.now()
            duration = focus_end - focus_start

            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"Hours: {int(hours)}, Minutes: {int(minutes)}, Seconds: {duration.seconds}")

            # End the focus session
            focusing = False

        # The extra 1.5 factor is to help prevent false positives
        elif focusing and distance > THRESHOLD * 1.5:
            print("Moving phone away!")
            # print(distance)





                
                




except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    arduino.close()  # Close the connection

