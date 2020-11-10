import asyncio

queue = None


async def start():
    while True:
        request = await queue.get()
        # TO-DO Process Website
        print("Request Received.")
        await asyncio.sleep(1)
        queue.task_done()


def init(loop):
    asyncio.set_event_loop(loop)
    global queue
    queue = asyncio.Queue()
    loop.run_until_complete(start())
