from .inku_control_service import InkubatorControlService
import asyncio

class InkuStreamService:

    def __init__(self):
        self.MESSAGE_STREAM_DELAY = 1
        self.MESSAGE_STREAM_RETRY_TIMEOUT = 15000

    async def event_generator(self):
        if InkubatorControlService.tempControl():
            yield {
                "event": "new_message",
                "id": "message_id",
                "retry": self.MESSAGE_STREAM_RETRY_TIMEOUT,
                "data": "message_content"
            }

        await asyncio.sleep(self.MESSAGE_STREAM_DELAY)
