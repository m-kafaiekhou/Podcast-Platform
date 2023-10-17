import json
import pika
import django
from sys import path
from os import environ

from .models import Notification
from podcast.models import Podcast


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


def callback_podcast_update(ch, method, properties, body):
    print("Received in likes...*****#*#*#**##****")
    data = json.loads(body)
    print(data, "*********###*#*#*#*#**##**")
    podcast = Podcast.objects.get(id=data['podcast'])

    users = data['users']

    notif_lst = []

    for user in users:
        notif = Notification(title='o', user_id=user, message=f'podcast {podcast.title} added new episodes')
        notif_lst.append(notif)

    ns = Notification.objects.bulk_create(notif_lst)
    print(ns, "ghghghghghghghghgjfjfjfj")
    print("update notif created successfully")
    


def auth_notif_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='auth-notification')
      
    channel.basic_consume(queue='auth-notification', on_message_callback=callback, auto_ack=True)
    print("Started Consuming...")
    channel.start_consuming()


def podcast_update_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

    print("be channel**********************************podcast_update**********")
    channel = connection.channel()
    print("af channel*************************************************")

    channel.queue_declare(queue='podcast_update')
            
    channel.basic_consume(queue='podcast_update', on_message_callback=callback_podcast_update, auto_ack=True)
    print("Started Consuming...")
    channel.start_consuming()

