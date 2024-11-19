# import asyncio
# import websockets
#
# # Handler for WebSocket connections
# async def echo(websocket):
#     print("Client connected")
#     try:
#         async for message in websocket:
#             print(f"Received from client: {message}")
#
#
#             # Echo message back to the client
#             # Will need to send the distance data here!
#             response = f"Server received: {message}"
#             await websocket.send(response)
#
#     except websockets.ConnectionClosed as e:
#         print(f"Connection closed: {e}")
#
# # Start the WebSocket server
# async def main():
#     host = "127.0.0.1"
#     port = 65432
#     print(f"Starting WebSocket server on {host}:{port}")
#     async with websockets.serve(echo, host, port):
#         await asyncio.Future()  # Run forever
#
# asyncio.run(main())



import asyncio
import websockets
from datetime import datetime

# List to manage connected clients
connected_clients = set()

# Handler for WebSocket connections
async def echo(websocket):
    print("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received from client: {message}")

            # Echo message back to the client
            response = f"Server received: {message}"
            await websocket.send(response)

    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        connected_clients.remove(websocket)
        print("Client disconnected")

# Function to send the current time to all connected clients every 5 seconds
async def send_time():
    while True:
        if connected_clients:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Broadcasting current time: {current_time}")
            # Broadcast the current time to all connected clients
            await asyncio.gather(
                *(client.send(f"Current time: {current_time}") for client in connected_clients)
            )
        await asyncio.sleep(5)  # Wait for 5 seconds before sending the next update

# Main function to start the server
async def main():
    host = "127.0.0.1"
    port = 65432
    print(f"Starting WebSocket server on {host}:{port}")
    async with websockets.serve(echo, host, port):
        # Run the server and the time sender concurrently
        await asyncio.gather(send_time())

asyncio.run(main())
