import json
import pika
import django
from sys import path
from os import environ

from .models import Notification


path.append('/home/Desktop/maktab/Podcast-Platform/PodcastPlatform/config/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 

django.setup()


def callback(ch, method, properties, body):
    print("Received in likes...")
    print(body)
    data = json.loads(body)
    print(data)
    user_id = data['user']

    if properties.content_type == 'login':
        Notification.objects.create(title='l', user_id=user_id, message=f'user with id {user_id} logged in')
        print("quote created")
    elif properties.content_type == 'registery':
        Notification.objects.create(title='r', user_id=user_id, message=f'user with id {user_id} just registered')
        print("quote updated")
    elif properties.content_type == 'refreshtoken':
        Notification.objects.create(title='t', user_id=user_id, message=f'user with id {user_id} requested for refresh token')
        print("quote deleted")


def auth_notif_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=600))

    print("be channel**************************************************")
    channel = connection.channel()
    print("af channel*************************************************")

    channel.queue_declare(queue='auth-notification')

            
    channel.basic_consume(queue='auth-notification', on_message_callback=callback, auto_ack=True)
    print("Started Consuming...")
    channel.start_consuming()
