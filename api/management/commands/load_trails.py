import json
from django.core.management.base import BaseCommand
from api.models import Trail

class Command(BaseCommand):
    help = 'Create or update trails from JSON data'

    def handle(self, *args, **kwargs):
        with open('/trek/trails.json') as f:
            data = json.load(f)

        for trail in data:
            Trail.objects.update_or_create(
                name=trail['name'],  # Use `name` as unique identifier
                defaults={
                    'region': trail['region'],
                    'description': trail['description'],
                    'distance_km': trail['distance_m'] / 1000,
                    'duration_days': trail['duration_days'],
                    'elevation': trail['elevation'],
                    'difficulty': trail['difficulty'],
                    'start_lat': trail['start_point']['lat'],
                    'start_lng': trail['start_point']['lng'],
                    'end_lat': trail['end_point']['lat'],
                    'end_lng': trail['end_point']['lng'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Trails created or updated successfully.'))
