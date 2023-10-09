import asyncio
import websockets
import random
import time

CLIENTS = set()

async def relay(queue, websocket):
    while True:
        # Implement custom logic based on queue.qsize() and
        # websocket.transport.get_write_buffer_size() here.
        message = await queue.get()
        await websocket.send(message)

def _get_some_data() -> str:
    # some logic to retrieve fragments of wav file, tbd
    return f"At {time.ctime()} got data : {random.randint(1,100)}"

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

def broadcast(message:str):
    if message:
        for queue in CLIENTS:
            queue.put_nowait(message)

async def broadcast_messages():
    while True:
        await asyncio.sleep(5)
        message = _get_some_data()  
        broadcast(message)


async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await broadcast_messages()  # runs forever

if __name__ == "__main__":
    asyncio.run(main())