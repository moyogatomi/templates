import pika


class RabbitConnection:
    def __init__(
        self,
        username=None,
        password=None,
        host=None,
        port=None,
        uri=None,
        routing_key=None,
        exchange=None,
    ):
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host, port, uri, credentials)
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=exchange, exchange_type="topic")

    def __enter__(self):
        return self.channel

    def __exit__(self, type, value, traceback):
        self.connection.close()