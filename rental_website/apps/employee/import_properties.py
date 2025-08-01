import csv
from django.core.management.base import BaseCommand
from .models import Property, Location

class Command(BaseCommand):
    help = "Import property data from CSV"

    def handle(self, *args, **kwargs):
        with open('apartments.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                loc_obj, _ = Location.objects.get_or_create(name=row['location'])
                Property.objects.create(
                    location=loc_obj,
                    bedrooms=int(row['bedrooms']),
                    bathrooms=int(row['bathrooms']),
                    price=int(row['price'])
                )
            self.stdout.write(self.style.SUCCESS('CSV data imported successfully.'))
            