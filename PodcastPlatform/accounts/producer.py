import json
import pika


def publish(method, body, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=600))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    properties = pika.BasicProperties(method, delivery_mode=2)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)
    connection.close()
