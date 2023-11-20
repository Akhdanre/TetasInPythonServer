import asyncio

from fastapi import WebSocket
from app.model.client_data import connected_inku_client, connected_user_client


class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str,  websocket: WebSocket):
        for connect in self.connections:
            if connect != websocket:
                await connect.send_text(message)
