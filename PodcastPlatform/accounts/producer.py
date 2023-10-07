import json
import pika


def publish(method, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=600))
    channel = connection.channel()
    channel.queue_declare(queue='auth-notification')
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='auth-notification', body=json.dumps(body), properties=properties)
    connection.close()

