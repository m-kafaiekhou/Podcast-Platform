from django.core.management.base import BaseCommand
from multiprocessing import Process

from accounts.consumer import auth_notif_consumer, podcast_update_consumer


class Command(BaseCommand):
    help = 'Launches Consumers : RabbitMQ'

    def handle(self, *args, **options):
        p1 = Process(target=auth_notif_consumer)
        p2 = Process(target=podcast_update_consumer)
        
        p1.start()
        p2.start()
        