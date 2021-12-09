from csv import DictReader
from datetime import datetime

from django.core.management.base import BaseCommand

from people.models import Person, PersonInfoPoint


class Command(BaseCommand):
    help = 'Imports persons from CSV'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        with open(options['filepath']) as file:
            reader = DictReader(file, delimiter='\t')

            for row in reader:
                person = Person.objects.create(
                    name=row.pop('name'),
                    birth_date=datetime.strptime(row.pop('birth_date'), '%d.%m.%Y'),
                    group=int(row.pop('group')),
                )

                for question, answer in row.items():
                    PersonInfoPoint.objects.create(
                        person=person,
                        heading=question,
                        info=answer,
                    )

                print(f'Created {person}')
