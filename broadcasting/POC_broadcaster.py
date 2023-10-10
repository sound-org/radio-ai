import asyncio
import websockets
import time
import os

CLIENTS = set()
FILENAME = "out.wav"

async def relay(queue, websocket):
    while True:
        # Implement custom logic based on queue.qsize() and
        # websocket.transport.get_write_buffer_size() here.
        message = await queue.get()
        print(f"[{time.ctime()}] broadcasting ... {message[:9]}")
        await websocket.send(message)

def _get_some_data() -> str:
    # some logic to retrieve fragments of wav file, tbd
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), FILENAME)
    return open(path, "rb").read()


async def handler(websocket):
    queue = asyncio.Queue()
    relay_task = asyncio.create_task(relay(queue, websocket))
    CLIENTS.add(queue)
    try:
        await websocket.wait_closed()
    finally:
        CLIENTS.remove(queue)
        relay_task.cancel()

async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass

def broadcast(message):
    if message:
        for queue in CLIENTS:
            queue.put_nowait(message)

async def broadcast_messages():
    while True:
        await asyncio.sleep(5)
        wave_file =_get_some_data() 
        broadcast(wave_file)


async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await broadcast_messages()  # runs forever

if __name__ == "__main__":
    asyncio.run(main())