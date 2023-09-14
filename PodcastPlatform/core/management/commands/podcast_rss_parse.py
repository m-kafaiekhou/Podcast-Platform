from django.core.management.base import BaseCommand
from parser.parsers import PodcastRSSParser
from podcast.models import Podcast, PodcastEpisode


class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        podcasts = Podcast.objects.all()
        try:
            for pod in podcasts:
                parser = PodcastRSSParser(pod, PodcastEpisode)

                parser.fill_db()
                
            self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully parsed and updated podcast data for all models)"
                    )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error while parsing and updating podcast rss data models \n {e})"
                )
            )
            
    