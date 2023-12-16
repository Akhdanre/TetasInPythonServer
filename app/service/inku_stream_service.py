import asyncio
import json
from fastapi import WebSocket, Depends
from sqlalchemy.orm import Session
from app.utils.deps import get_db
from app.model import models


class ConnectionManager:
    def __init__(self):
        self.connections = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def on_message(self, message: str, websocket: WebSocket, db: Session):
        data = json.loads(message)

        if data["action"] == "send":
            await self.broadcast(message, websocket)

        elif data["action"] == "get":
            if data["request"] == "info_inku":
                response = self.get_temp_and_humd(db)
                response_message = {
                    "sender": "server",
                    "action": "send_info",
                    "data": response
                }
                await self.send_personal_message(json.dumps(response_message), websocket)

        elif data["action"] == "get":
            if data["request"] == "info_limit":
                response = self.get_temp_and_humd_limit(db)
                response_message = {
                    "sender": "server",
                    "action": "send_limit",
                    "data": response
                }
                await self.send_personal_message(json.dumps(response_message), websocket)

        elif data["action"] == "post":
            if data["request"] == "send_data":
                temp = data["data"]["temp"]
                humd = data["data"]["humd"]
                water = data["data"]["water"]

                self.set_temp_and_humd(temp, humd, water, db)

                await self.broadcast(message, websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, websocket: WebSocket):
        for connect in self.connections:
            if connect != websocket:
                await connect.send_text(message)

    def set_temp_and_humd(self, temp: int, humd: int, water: int, db: Session):
        exist_inku = db.query(models.InkubatorsModel).filter_by(
            id="INK0001").first()

        if exist_inku:
            exist_inku.humd_value = humd
            exist_inku.temp_value = temp
            exist_inku.water_volume = water

            db.commit()
            db.refresh(exist_inku)

    def get_temp_and_humd(self, db: Session):
        exist_inku = db.query(models.InkubatorsModel).filter_by(
            id="INK0001").first()
        if exist_inku:
            return {
                "temp": exist_inku.temp_value,
                "humd": exist_inku.humd_value,
                "water": exist_inku.water_volume
            }
        return None

    def get_temp_and_humd_limit(self, db: Session):
        exist_inku = db.query(models.InkubatorsModel).filter_by(
            id="INK0001").first()
        if exist_inku:
            return {
                "temp": exist_inku.temp_limit,
                "humd": exist_inku.humd_limit,
            }
        return None
