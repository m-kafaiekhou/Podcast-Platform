from django.core.management.base import BaseCommand

from parser.tasks import podcast_parse_task


class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        try:
            res = podcast_parse_task.delay()
            
                
            self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully parsed and updated podcast data for all models"
                    )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error while parsing and updating podcast rss data models \n {e})"
                )
            )
            
    