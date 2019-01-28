from django.core.management.base import BaseCommand
import csv
import os
from django.conf import settings


from ...models import Package


class Command(BaseCommand):
    help = 'Add Default Groups'

    def _populate(self):

        file_path = os.path.join(settings.STATIC_ROOT + "/csv" +"/finaldatasets.csv")
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            i=1

            for row in reader:
                p = Package(name=row['Name of Package '],
                            price=row[' Price '],
                            duration = row[' Duration '],
                            rating=row[' Rating '],
                            tourtype = row[' Tour Type '],
                            trekdifficulty = row[' Trek Difficulty '],
                            operator = row[' Operator '],
                            location = row[' Location '],
                            primary_activity = row[' Primary Activity '],
                            secondary_activity = row[' Secondary Activity '])
                p.save()



    def handle(self, *args, **options):
        self._populate()
        print('Database populated !!')

