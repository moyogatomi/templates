import asyncio
import json
import logging
import random
import time
import uuid
from typing import List, Optional

from aio_pika import ExchangeType, IncomingMessage, Message, connect
from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from dramatiq_conf import dramatiq, rabbitmq_broker
from pikclient import close_rabbit_connection, connect_to_rabbit, get_database

logger = logging.getLogger("uvicorn.info")
app = FastAPI()
origins = [
    "http://localhost:8080",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except:
            logger.error("Failed to send message")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.get("/create_task")
async def get():

    message_identifier = str(uuid.uuid4())
    timestamp = int(time.time() * 1000)
    msg = dramatiq.Message(
        queue_name="worker_queue",
        actor_name="task",
        args=({"task_id": message_identifier, "user_id": "default"},),
        kwargs={},
        options={},
        message_id=message_identifier,
        message_timestamp=timestamp,
    )

    channel = await get_database()
    # channel = await connection.channel()
    exchange = await channel.declare_exchange("topic_logs", ExchangeType.TOPIC)
    message_body = json.dumps(
        dict(
            state="queued",
            progress=0,
            user_id="default",
            task_id=message_identifier,
            message_type="task",
        )
    ).encode()
    message = Message(message_body)
    await exchange.publish(
        message,
        routing_key="default.task",
    )
    return rabbitmq_broker.enqueue(msg)  # .get_result(block=False, timeout=10000)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    user_id = "default"

    # fake tab_id
    tab_id = random.randint(0, 10000)

    queue_user = f"{user_id}-{tab_id}"
    queue_name = f"events_{queue_user}"

    # For more complex behaviour, we can remove .task and receive all events and sort them here
    routing_key = f"{user_id}.task"

    async def on_message(message: IncomingMessage):
        logger.info("received message")
        await manager.send_message(json.loads(message.body), websocket)

    try:
        channel = await get_database()
        # channel = await connection.channel()
        exchange = await channel.declare_exchange(
            "topic_logs",
            ExchangeType.TOPIC,
        )

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        # Binding the queue to the exchange
        await queue.bind(exchange, routing_key)
        consumer_tag = await queue.consume(on_message, no_ack=True)

        while True:

            data = await websocket.receive_text()
            x = await manager.send_message(data, websocket)

    except Exception as e:
        logger.info("Websocket Disconnect")
        logger.error(str(e))
        manager.disconnect(websocket)

    await queue.cancel(consumer_tag)
    await queue.unbind(exchange, routing_key)

    # No channel disconnection as there is 1 channel and 1 connection per application (asyncio)
    ## await channel.close()

    logger.info("Ending websocket")


app.add_event_handler("startup", connect_to_rabbit)
app.add_event_handler("shutdown", close_rabbit_connection)
