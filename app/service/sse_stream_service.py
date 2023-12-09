import asyncio
from app.model import connected_user_client


class SSEStreamService():

    async def event_generator_mobile(self, request, user_id, token):
        client_queue = asyncio.Queue()
        connected_user_client[user_id] = [token, client_queue]

        try:
            while True:
                if await request.is_disconnected():
                    break
                message = await client_queue.get()
                if message:
                    yield message
                await asyncio.sleep(1)
        finally:
            connected_user_client.pop(user_id)
