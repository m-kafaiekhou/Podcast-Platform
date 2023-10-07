from django.core.management.base import BaseCommand
from accounts.consumer import auth_notif_consumer


class Command(BaseCommand):
    help = 'Launches Consumer for login message : RabbitMQ'

    def handle(self, *args, **options):
        auth_notif_consumer()
        