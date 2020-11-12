import asyncio
import os
import sys

from channels.db import database_sync_to_async

queue = None


async def start():
    while True:
        if not queue.empty():
            request = await queue.get()
            sys.stdout.write("Request Received.\n")
            request.status = 0
            await database_sync_to_async(request.save)()
            await asyncio.sleep(1)
            files_dir = os.getcwd() + os.pathsep + 'files'
            if not os.path.isdir(files_dir):
                os.mkdir(files_dir)
            req_dir = files_dir + os.pathsep + request.req_id
            if not os.path.isdir(req_dir):
                os.mkdir(req_dir)
            images_file = req_dir + os.pathsep + 'images.txt'
            if os.path.isfile(images_file):
                os.remove(images_file)
            # TO-DO Process Website
            f = open(images_file, 'w')
            f.write('Test\nRequest Id:' + request.req_id)
            f.close()
            request.path = images_file
            request.status = 1
            await database_sync_to_async(request.save)()
            sys.stdout.write("Status 1.\n")
            queue.task_done()


def init(loop):
    asyncio.set_event_loop(loop)
    global queue
    queue = asyncio.Queue()
    loop.run_until_complete(start())
