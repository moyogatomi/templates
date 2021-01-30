import dramatiq
import pika
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

result_backend_connection = "redis://redis:password_test@redis_backend:6379/0"
broker_connection = "amqp://rabbitmq:rabbitmq@rabbit:5672"

result_backend = RedisBackend(url=result_backend_connection)
rabbitmq_broker = RabbitmqBroker(url=broker_connection)
rabbitmq_broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(rabbitmq_broker)