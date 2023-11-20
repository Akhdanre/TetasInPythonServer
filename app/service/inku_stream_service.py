import asyncio

from fastapi import WebSocket
from app.model.client_data import connected_inku_client, connected_user_client


# class InkuStreamService:
#     def __init__(self):
#         self.STREAM_DELAY = 1
#         self.MESSAGE_STREAM_RETRY_TIMEOUT = 15000

#     async def event_generator_inku(self, request, inku_id, token):
#         client_queue = asyncio.Queue()
#         connected_inku_client[inku_id] = [token, client_queue]
#         try:
#             while True:
#                 if await request.is_disconnected():
#                     break
#                 message = await client_queue.get()
#                 if message:
#                     yield message
#                 await asyncio.sleep(self.STREAM_DELAY)
#         finally:
#             connected_inku_client.pop(inku_id)

#     async def event_generator_mobile(self, request, user_id, token):
#         client_queue = asyncio.Queue()
#         connected_user_client[user_id] = [token, client_queue]
#         try:
#             while True:
#                 if await request.is_disconnected():
#                     break
#                 message = await client_queue.get()
#                 if message:
#                     yield message
#                 await asyncio.sleep(self.STREAM_DELAY)
#         finally:
#             connected_user_client.pop(user_id)

class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)
