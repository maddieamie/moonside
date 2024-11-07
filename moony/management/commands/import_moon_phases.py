from django.core.management.base import BaseCommand
import csv
from moonside.models import MoonPhase
from datetime import datetime, time

class Command(BaseCommand):
    help = 'Import moon phase data from a CSV file'

    def add_arguments(self, parser):
        # Add the CSV file path as a command-line argument
        parser.add_argument(
            'relative_csv_path',
            type=str,
            help='The relative or absolute path to the CSV file containing moon phase data'
        )

    def handle(self, *args, **options):
        # Get the CSV file path from the options
        csv_path = options['relative_csv_path']
        
            # Default times for sunrise and sunset
        default_sunrise = time(7, 0)  # 7:00 AM
        default_sunset = time(17, 0)  # 5:00 PM
        
        # Open the CSV file at the specified path
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Adjust based on your CSV structure
                date = datetime.strptime(row['Date'], '%m/%d/%Y').date()
                phase = row['Phase']
                moonrise = datetime.strptime(row['Moonrise'], '%I:%M %p').time() if row['Moonrise'] and row['Moonrise'] != '-' else None
                moonset = datetime.strptime(row['Moonset'], '%I:%M %p').time() if row['Moonset'] and row['Moonset'] != '-' else None
                illumination = int(float(row['Illumination'].replace('%', ''))) if row['Illumination'] and row['Illumination'] != '-' else None

                # Create or update MoonPhase records
                MoonPhase.objects.update_or_create(
                    date=date,
                    defaults={
                        'phase': phase,
                        'moonrise': moonrise,
                        'moonset': moonset,
                        'illumination': illumination,
                        'sunrise': default_sunrise,
                        'sunset': default_sunset
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_path}'))
