from django.core.management.base import BaseCommand
import csv
import os

from ...models import Package


class Command(BaseCommand):
    help = 'Add Default Groups'

    def _populate(self):
        # with open(os.path.dirname(os.path.dirname(__file__))+'/finaldatasets.csv') as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         created = Package.objects.get_or_create(
        #             name=row[0],
        #             price=row[1],
        #             duration=row[2],
        #             rating=row[3],
        #             tourtype=row[4],
        #             trekdifficulty=row[5],
        #             operator=row[6],
        #             location=row[7],
        #             primary_activity=row[8],
        #             secondary_activity=row[9],
        #         )

        with open(os.path.dirname(os.path.dirname(__file__))+'/finaldatasets.csv') as csvfile:
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
                            secondary_activty = row[' Secondary Activity '])
                p.save()



    def handle(self, *args, **options):
        self._populate()
        print('Database populated !!')

