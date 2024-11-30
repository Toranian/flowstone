from functions import App
import asyncio


if __name__ == '__main__':

    app = App()

    print("Starting relay server")
    asyncio.run(app.socket.start())


    asyncio.run_coroutine_threadsafe(app.socket.send_countdown(10), asyncio.get_event_loop())


