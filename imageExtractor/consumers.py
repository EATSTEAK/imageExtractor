import asyncio

from channels.generic.websocket import WebsocketConsumer
from imageExtractor.models import Request
import json


class RequestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("Connection Received.")

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        self.send(json.dumps({
            'message': 'Connection Established.'
        }))
