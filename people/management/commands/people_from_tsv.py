from csv import DictReader
from datetime import datetime
from pathlib import Path

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand

from people.models import Person, PersonInfoPoint

PHOTOS_FOLDER = Path('photos/')


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

                photo_path = row.pop('photo', None)
                if photo_path:
                    with open(PHOTOS_FOLDER / photo_path, 'rb') as photo:
                        img = ImageFile(photo)
                        person.photo.save(photo_path, img)

                for question, answer in row.items():
                    if not question or not answer:
                        print(f'Skipping empty question "{question}": "{answer}"')
                        continue

                    PersonInfoPoint.objects.create(
                        person=person,
                        heading=question,
                        info=answer,
                    )

                print(f'Created {person}')
