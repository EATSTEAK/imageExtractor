from django.db import models
from django.utils import timezone
from imageExtractor import queue_worker


class Request(models.Model):
    req_id = models.UUIDField()
    url = models.TextField()
    status = models.IntegerField()
    created = models.DateTimeField()

    def add_to_queue(self):
        # -1: IN QUEUE, 0: PROCESSING, 1: FINISHED
        self.status = -1
        self.created = timezone.now()
        self.save()
        queue_worker.queue.put(self)

    def __str__(self):
        return self.req_id.__str__
