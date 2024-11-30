import serial
import asyncio
from ewma import EWMA
from datetime import datetime
from sock import WebSocketServer
import time

THRESHOLD = 2.5
MAX_DISTANCE = 15
GRACE_PERIOD = 20  # After placing the phone down, the user has 20 seconds to pick it back up.

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
focusing = False
distracted = False
ewma = EWMA()
session_length = 10
focus_start = datetime.now()


def send_rgb(r, g, b, intensity=1):
    """Send RGB values to the Arduino."""
    r = int(r * intensity)
    g = int(g * intensity)
    b = int(b * intensity)
    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
        rgb_data = f"{r},{g},{b}\n"
        arduino.write(rgb_data.encode())
        print(f"Sent: {rgb_data.strip()}")
    else:
        print("Error: RGB values must be between 0 and 255.")


def clear_led():
    """Turn off the LED."""
    send_rgb(0, 0, 0)


async def monitor_focus(server):
    """Monitor the user's focus and manage the LED state."""
    global focusing, distracted, session_length, focus_start
    try:
        while True:
            try:
                line = arduino.readline().decode().strip()
                distance = float(line)
            except ValueError:
                # Ignore invalid data
                continue

            if distance < THRESHOLD and not focusing:
                focusing = True

                if len(ewma.actual) == 0:
                    session_length = 10
                else:
                    session_length = ewma.adjust(session_length)

                print(f"Starting session for {session_length}")

                await server.send_message(f"Starting session for {session_length}")

                send_rgb(0, 0, 255)

                focus_start = datetime.now()

            elif focusing and distance > MAX_DISTANCE:
                print("You've moved your device, and your focus session is forfeit.")
                focus_end = datetime.now()
                duration = focus_end - focus_start

                # if duration.total_seconds() < GRACE_PERIOD:
                #     print("Grace period not over yet.")
                #     continue

                hours, remainder = divmod(duration.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                print(f"Hours: {int(hours)}, Minutes: {int(minutes)}, Seconds: {duration.seconds % 60}")

                # Blink the LEDs to indicate the session is over.
                clear_led()
                time.sleep(0.5)
                send_rgb(255, 0, 0, 0.2)
                time.sleep(0.5)
                clear_led()

                send_rgb(255, 0, 0)
                time.sleep(0.5)
                clear_led()

                send_rgb(255, 0, 0)
                time.sleep(0.5)
                clear_led()

                # End the focus session
                focusing = False
                clear_led()

            # Need to make sure this doesn't constantly trigger.
            elif focusing and distance < THRESHOLD and distracted:
                send_rgb(0, 0, 255)
                distracted = False

            # The extra 1.5 factor is to help prevent false positives
            elif focusing and distance > THRESHOLD * 1.5 and distance < MAX_DISTANCE:
                print("Moving phone away!")
                # print(distance)

                intensity = (distance / MAX_DISTANCE)
                # print(f"Intensity: {intensity}"))
                send_rgb(255, 0, 0, intensity)
                distracted = True


            await asyncio.sleep(0.1)  # Avoid excessive CPU usage

    except KeyboardInterrupt:
        print("Monitoring interrupted.")

    finally:
        arduino.close()  # Close the connection


async def main():
    server = WebSocketServer()
    
    # Start the WebSocket server in the background
    server_task = asyncio.create_task(server.start())

    # Send an initial message to WebSocket clients
    await asyncio.sleep(1)
    await server.send_message("Hello, WebSocket clients!")

    # Start monitoring focus concurrently
    monitor_task = asyncio.create_task(monitor_focus(server))

    try:
        # Keep the server running and handle monitoring
        await asyncio.gather(server_task, monitor_task)
    except asyncio.CancelledError:
        print("Tasks cancelled. Exiting.")
    finally:
        arduino.close()  # Ensure Arduino connection is closed


if __name__ == "__main__":
    asyncio.run(main())
