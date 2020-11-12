import asyncio
import sys

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from imageExtractor.models import Request
import json


class RequestConsumer(AsyncWebsocketConsumer):
    connected = False

    async def connect(self):
        await self.accept()
        print("Connection Received.")
        self.connected = True
        await self.send(json.dumps({
            'message': '다른 작업이 완료될 때까지 대기 중입니다...',
            'status': -1
        }))

        status = -1
        while self.connected:
            await asyncio.sleep(2)
            sys.stdout.write('Check Requests\n')
            requests = await database_sync_to_async(self.get_session_request)()
            if not await database_sync_to_async(self.session_is_unique)(requests):
                await self.send(json.dumps({
                    'message': '올바르지 않은 세션입니다. 연결을 종료합니다...',
                    'status': -2
                }))
                await self.websocket_disconnect('연결이 종료되었습니다.')
                break
            request = await database_sync_to_async(self.get_request)(requests)
            req_status = await database_sync_to_async(self.request_status)(request)
            sys.stdout.write(str(req_status) + '\n')
            if status is not req_status:
                status = req_status
                if status == 0:
                    await self.send(json.dumps({
                        'message': '처리 중입니다...',
                        'status': 0
                    }))
                elif status == 1:
                    await self.send(json.dumps({
                        'message': '처리가 완료되었습니다.',
                        'status': 1
                    }))
                    await self.websocket_disconnect('연결이 종료되었습니다.')
                    break

    def get_session_request(self):
        return Request.objects.filter(req_id=self.scope['url_route']['kwargs']['req_id'])

    def session_is_unique(self, requests):
        return requests.exists() and len(requests) == 1

    def get_request(self, requests):
        return requests[0]

    def request_status(self, request):
        return request.status

    async def disconnect(self, code):
        self.connected = False

    async def receive(self, text_data):
        await self.send(json.dumps({
            'message': 'Connection Established.'
        }))
