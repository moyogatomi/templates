import logging

import asyncio
from aio_pika import connect, IncomingMessage, ExchangeType


RABBIT_URL = "amqp://rabbitmq:rabbitmq@rabbit:5672/"


class Broker:
    connection = None


broker = Broker()


async def connect_to_rabbit():
    logging.info("Connecting to rabbit")
    # loop = asyncio.get_event_loop()
    # asyncio.ensure_future(main(loop))
    broker.connection = await connect(
        RABBIT_URL, loop=asyncio.get_running_loop()
    )  # , loop=loop)


async def close_rabbit_connection():
    logging.info("Closing connection")
    broker.connection.close()
    logging.info("Closed connection")


async def get_database():
    return broker.connection
