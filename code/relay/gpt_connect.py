import serial
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from sock import WebSocketServer

THRESHOLD = 2.5
MAX_DISTANCE = 15

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
focusing = False
distracted = False
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


def focus_monitor():
    """Blocking function to monitor focus."""
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
                print(f"Starting session for {session_length} seconds.")
                send_rgb(0, 0, 255)
                focus_start = datetime.now()

            elif focusing and distance > MAX_DISTANCE:
                print("Focus session ended prematurely.")
                clear_led()
                focusing = False

            elif focusing and distance > THRESHOLD * 1.5 and distance < MAX_DISTANCE:
                print("Distracted! Adjusting intensity.")
                intensity = (distance / MAX_DISTANCE)
                send_rgb(255, 0, 0, intensity)
                distracted = True

            elif focusing and distance < THRESHOLD and distracted:
                send_rgb(0, 0, 255)
                distracted = False

    except Exception as e:
        print(f"Error in focus_monitor: {e}")
    finally:
        arduino.close()


async def main():
    server = WebSocketServer()

    # Start the WebSocket server
    server_task = asyncio.create_task(server.start())

    # Run the focus monitor in a separate thread
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        focus_monitor_task = loop.run_in_executor(executor, focus_monitor)

        try:
            # Keep both tasks running
            await asyncio.gather(server_task, focus_monitor_task)
        except asyncio.CancelledError:
            print("Tasks cancelled. Exiting.")
        finally:
            arduino.close()


if __name__ == "__main__":
    asyncio.run(main())
