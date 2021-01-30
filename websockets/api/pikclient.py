import logging

import asyncio
from aio_pika import connect_robust, IncomingMessage, ExchangeType


RABBIT_URL = "amqp://rabbitmq:rabbitmq@rabbit:5672/"


class Broker:
    connection = None
    channel = None


broker = Broker()


async def connect_to_rabbit():
    logging.info("Connecting to rabbit")

    broker.connection = await connect_robust(
        RABBIT_URL, loop=asyncio.get_running_loop()
    )  # , loop=loop)

    broker.channel = await broker.connection.channel()


async def close_rabbit_connection():
    logging.info("Closing connection")
    broker.connection.close()
    logging.info("Closed connection")


async def get_database():
    return broker.channel
