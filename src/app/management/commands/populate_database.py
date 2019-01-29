from django.core.management.base import BaseCommand
import csv
import os
import re
from django.conf import settings


from ...models import Package


class Command(BaseCommand):
    help = 'Add Default Groups'

    def _populate(self):

        file_path = os.path.join(settings.STATIC_ROOT + "/csv" +"/finaldatasets.csv")
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)


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
                            secondary_activity = row[' Secondary Activity '],
                            image=row[' Image '])
                p.save()
        print('Description Remaining...')


    def _populate_description(self):

        file_path = os.path.join(settings.STATIC_ROOT + "/csv" + "/description.csv")
        f = open(file_path, "r")
        lines = f.read().strip().split("#####")

        for i in lines:
            j = 1
            p = Package.objects.get(id=j)
            line = re.sub(r"[\n\t]*", "", i)
            p.description = line
            p.save()
            if j > 532:
                break
        print('Description completed... !!')



    def handle(self, *args, **options):
        self._populate()
        self._populate_description()
        print('Database populated !!')

