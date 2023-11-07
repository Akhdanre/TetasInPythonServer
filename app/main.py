import asyncio
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

class Item(BaseModel):
    message: str

app = FastAPI()

messages = []


@app.post("/api/value")
async def value(item: Item):
    global messages
    messages.append(item.message)
    return {"status": "ok",
         "condition" : True}

STREAM_DELAY = 1
RETRY_TIMEOUT = 15000

def new_messages():
    return bool(messages)

async def event_generator():
    while True:
        await asyncio.sleep(STREAM_DELAY)

        if new_messages():
            message = messages.pop(0)
            yield {
                "event": "new_message",
                "id": "message_id",
                "data": f"data yang dikirim adalah {message}"
            }

@app.get('/stream')
async def message_stream(request: Request):
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
