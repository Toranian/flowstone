from functions import App
import asyncio


if __name__ == '__main__':

    app = App()

    print("Starting relay server")
    asyncio.run(app.socket.start())
