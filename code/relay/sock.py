import asyncio
import websockets
from datetime import datetime

class WebSocketServer:
    def __init__(self, host='127.0.0.1', port=65432):
        # self.host = host
        # self.port = port

        self.host = "ws://flowstone-production.up.railway.app/socket"
        self.port = 65432
        self.connected_clients = set()

    async def echo(self, websocket):
        print("Client connected")
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                print(f"Received from client: {message}")

                # Echo message back to the client
                response = f"Server received: {message}"
                await websocket.send(response)

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        finally:
            self.connected_clients.remove(websocket)
            print("Client disconnected")

    async def send_time(self):
        while True:
            if self.connected_clients:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Broadcasting current time: {current_time}")
                # Broadcast the current time to all connected clients
                await asyncio.gather(
                    *(client.send(f"Current time: {current_time}") for client in self.connected_clients)
                )
            await asyncio.sleep(5)  # Wait for 5 seconds before sending the next update

    async def start(self):
        print(f"Starting WebSocket server on {self.host}:{self.port}")
        async with websockets.serve(self.echo, self.host, self.port):
            # Run the server and the time sender concurrently
            await asyncio.gather(self.send_time())


# Running the server
if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start())

