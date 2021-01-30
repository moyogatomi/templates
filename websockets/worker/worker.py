import logging
import os
import time
from dramatiq_conf import dramatiq
import pika
from rabbit_utils import RabbitConnection
import json
import random

logging.getLogger("dramatiq tasks").setLevel(logging.INFO)
worker_queue = "worker_queue"


class Job:
    """Pseudo job."""

    def __init__(self, task_id, user_id):
        self.state = "received"
        self.progress = 0
        self.task_id = task_id
        self.user_id = user_id
        self.done = False

    def work(self):
        if self.progress >= 100:
            self.done = True
            return True

        if self.state == "in progress":
            self.state = "computing"

        if self.state == "received":
            self.state = "in progress"

        random_sleep = random.randint(1, 10) / 10
        time.sleep(random_sleep)
        self.progress += int(random_sleep * 10)
        if self.progress >= 100:
            self.progress = 100
            self.state = "done"
            return True
        else:
            return False

    def get_state(self):
        return dict(
            state=self.state,
            progress=self.progress,
            user_id=self.user_id,
            task_id=self.task_id,
            message_type="task",
        )


@dramatiq.actor(
    store_results=True,
    queue_name=worker_queue,
    max_age=120 * 1000,
    time_limit=120 * 1000,
)
def task(payload: str):

    # should come with request
    user_id = payload.get("user_id")
    task_id = payload.get("task_id")

    # Routing key (user) in order to publish messages to specific user
    routing_key = f"{user_id}.task"

    job = Job(task_id, user_id)

    # json.dumps(message)
    with RabbitConnection(
        username="rabbitmq",
        password="rabbitmq",
        host="rabbit",
        port="5672",
        uri="/",
        routing_key=routing_key,
        exchange="topic_logs",
    ) as channel:

        channel.basic_publish(
            exchange="topic_logs",
            routing_key=routing_key,
            properties=pika.BasicProperties(
                expiration="60000",
            ),
            body=json.dumps(job.get_state()),
        )

        logging.info(f"Initiated task")
        while True:
            result = job.work()
            channel.basic_publish(
                exchange="topic_logs",
                routing_key=routing_key,
                properties=pika.BasicProperties(
                    expiration="15000",
                ),
                body=json.dumps(job.get_state()),
            )
            if result:
                break

    return {}