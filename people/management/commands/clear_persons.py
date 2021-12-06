from django.core.management.base import BaseCommand

from people.models import Person


class Command(BaseCommand):
    help = 'Deletes all persons'

    def handle(self, *args, **options):
        Person.objects.all().delete()
