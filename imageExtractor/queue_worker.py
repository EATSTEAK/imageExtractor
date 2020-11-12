import asyncio
import os
import shutil
import sys

from channels.db import database_sync_to_async
from django.utils import timezone

from imageExtractor import image_crawler

queue = None


async def start():
    while True:
        if not queue.empty():
            await database_sync_to_async(clean_requests)()
            request = await queue.get()
            sys.stdout.write("Request Received.\n")
            request.status = 0
            await database_sync_to_async(request.save)()
            await asyncio.sleep(1)
            files_dir = os.path.join(os.getcwd(), 'files')
            if not os.path.isdir(files_dir):
                os.mkdir(files_dir)
            req_dir = os.path.join(files_dir, str(request.req_id))
            if not os.path.isdir(req_dir):
                os.mkdir(req_dir)
            images_file = os.path.join(req_dir, 'images.zip')
            await image_crawler.find_all_images_and_save(request)
            if not os.path.isfile(images_file):
                request.status = -2
                sys.stdout.write("No file.\n")
            else:
                request.path = images_file
                request.status = 1
                sys.stdout.write("Success.\n")
            await database_sync_to_async(request.save)()
            queue.task_done()


def clean_requests():
    from imageExtractor.models import Request
    queryset = Request.objects.filter(created__lte=(timezone.now() - timezone.timedelta(minutes=5)))
    files_dir = os.path.join(os.getcwd(), 'files')
    for query in queryset:
        req_dir = os.path.join(files_dir, str(query.req_id))
        if os.path.isdir(req_dir):
            shutil.rmtree(req_dir)
        query.delete()


def init(loop):
    asyncio.set_event_loop(loop)
    global queue
    queue = asyncio.Queue()
    loop.run_until_complete(start())
