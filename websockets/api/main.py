from typing import List
from typing import Optional
import time
from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    status,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse
import json
import random
import asyncio

app = FastAPI()


class FakeTask:
    def __init__(self, num_tasks):
        self.num_tasks = num_tasks
        self.tasks = {i: {"progress": 0, "state": "started"} for i in range(num_tasks)}

    def __call__(self):
        key = random.randint(0, self.num_tasks - 1)
        if self.tasks[key]["progress"] == 0:
            self.tasks[key]["progress"] += 1
            return {(key): {"progress": 0, "state": "started"}}
        else:
            if self.tasks[key]["progress"] > 0 and self.tasks[key]["progress"] <= 30:
                self.tasks[key]["state"] = "in progress"
            elif self.tasks[key]["progress"] > 30 and self.tasks[key]["progress"] < 99:
                self.tasks[key]["state"] = "computing"
            else:
                self.tasks[key]["state"] = "done"
                self.tasks[key]["progress"] = 99
        self.tasks[key]["progress"] += 1
        return {(key): self.tasks[key]}


fake = FakeTask(10)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def send_message(self, message: dict, websocket: WebSocket):
        websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return 200


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Entering")
    await manager.connect(websocket)
    print("got conn")
    try:
        # data = await websocket.receive_text()
        while True:
            # data = await websocket.receive_text()
            print("sendinf...")
            data = fake()
            x = await manager.send_personal_message(data, websocket)
            print("JUST SEND", data)
            # await manager.broadcast(f"Client # says: {data}")
            # print("broadcast")
            await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client # left the chat")